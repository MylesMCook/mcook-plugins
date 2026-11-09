#!/usr/bin/env python3
"""Bounded REST operations for a Grist AppEvents logging document."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


PLAN_VERSION = 1
DEFAULT_TABLE = "AppEvents"
DEFAULT_MAX_INPUT_BYTES = 1_000_000
MAX_VERIFY_REQUEST_PATH_BYTES = 4_096
EVENT_COLUMNS = (
    ("EventId", "Text", "Event ID"),
    ("OccurredAt", "Text", "Occurred at"),
    ("Source", "Text", "Source"),
    ("Environment", "Text", "Environment"),
    ("EventType", "Text", "Event type"),
    ("Payload", "Text", "Payload JSON"),
)
EVENT_FIELD_IDS = tuple(column_id for column_id, _, _ in EVENT_COLUMNS)
READ_ONLY_SQL = re.compile(r"^(?:select|with)\b", re.IGNORECASE)
FORBIDDEN_SQL = re.compile(
    r"\b(?:insert|update|delete|replace|create|drop|alter|attach|detach|pragma|vacuum)\b",
    re.IGNORECASE,
)


class GristOpsError(RuntimeError):
    """An expected, safe-to-report failure."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        raise GristOpsError(f"refusing authenticated redirect ({code}) to {newurl}")


@dataclass(frozen=True)
class Settings:
    url: str
    doc_id: str
    token: str

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Settings":
        url = (args.url or os.environ.get("GRIST_URL", "")).rstrip("/")
        doc_id = args.doc_id or os.environ.get("GRIST_DOC_ID", "")
        token = args.token or os.environ.get("GRIST_TOKEN", "")
        parsed_url = urlsplit(url)
        if parsed_url.scheme not in {"https", "http"} or not parsed_url.hostname:
            raise GristOpsError("GRIST_URL must start with https:// or http://")
        if parsed_url.username or parsed_url.password or parsed_url.query or parsed_url.fragment:
            raise GristOpsError("GRIST_URL must not contain credentials")
        if parsed_url.scheme == "http" and parsed_url.hostname.lower() not in {"localhost", "127.0.0.1", "::1"}:
            raise GristOpsError("GRIST_URL must use HTTPS unless it is a loopback address")
        if not doc_id:
            raise GristOpsError("GRIST_DOC_ID is required")
        if not token:
            raise GristOpsError("GRIST_TOKEN is required")
        return cls(url=url, doc_id=doc_id, token=token)


class GristClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.opener = build_opener(NoRedirect())

    def request(self, method: str, path: str, payload: Any | None = None) -> Any:
        body = None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.settings.token}",
        }
        if payload is not None:
            body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(
            f"{self.settings.url}{path}", data=body, headers=headers, method=method
        )
        try:
            with self.opener.open(request, timeout=20) as response:
                raw = response.read()
        except GristOpsError:
            raise
        except HTTPError as error:
            raise GristOpsError(f"Grist API {error.code}") from error
        except URLError as error:
            raise GristOpsError(f"could not reach Grist: {error.reason}") from error
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError as error:
            raise GristOpsError("Grist returned a non-JSON response") from error

    def path(self, suffix: str) -> str:
        return f"/api/docs/{quote(self.settings.doc_id, safe='')}{suffix}"

    def tables(self) -> list[dict[str, Any]]:
        response = self.request("GET", self.path("/tables"))
        tables = response.get("tables") if isinstance(response, dict) else None
        if not isinstance(tables, list):
            raise GristOpsError("Grist returned an invalid tables response")
        return [table for table in tables if isinstance(table, dict)]

    def columns(self, table: str) -> list[dict[str, Any]]:
        response = self.request("GET", self.path(f"/tables/{quote(table, safe='')}/columns"))
        columns = response.get("columns") if isinstance(response, dict) else None
        if not isinstance(columns, list):
            raise GristOpsError("Grist returned an invalid columns response")
        return [column for column in columns if isinstance(column, dict)]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def write_result(value: Any, pretty: bool) -> None:
    indent = 2 if pretty else None
    print(json.dumps(value, indent=indent, sort_keys=True, ensure_ascii=True))


def current_schema(client: GristClient, table: str) -> dict[str, Any]:
    known_tables = {item.get("id") for item in client.tables()}
    if table not in known_tables:
        return {"table": table, "exists": False, "columns": {}}

    columns: dict[str, str] = {}
    for item in client.columns(table):
        column_id = item.get("id")
        fields = item.get("fields", {})
        if isinstance(column_id, str) and isinstance(fields, dict):
            column_type = fields.get("type", "Any")
            columns[column_id] = str(column_type)
    return {"table": table, "exists": True, "columns": columns}


def schema_digest(schema: dict[str, Any]) -> str:
    material = {
        "exists": schema["exists"],
        "table": schema["table"],
        "columns": dict(sorted(schema["columns"].items())),
    }
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def expected_columns() -> list[dict[str, Any]]:
    return [
        {"id": column_id, "fields": {"type": column_type, "label": label}}
        for column_id, column_type, label in EVENT_COLUMNS
    ]


def build_schema_plan(schema: dict[str, Any]) -> dict[str, Any]:
    conflicts: list[dict[str, str]] = []
    additions: list[dict[str, Any]] = []
    for column in expected_columns():
        column_id = column["id"]
        expected_type = column["fields"]["type"]
        actual_type = schema["columns"].get(column_id)
        if actual_type is None:
            additions.append(column)
        elif actual_type != expected_type:
            conflicts.append(
                {"column": column_id, "expected": expected_type, "actual": actual_type}
            )

    if conflicts:
        operations: list[dict[str, Any]] = []
    elif not schema["exists"]:
        operations = [{"action": "create_table", "table": schema["table"], "columns": expected_columns()}]
    elif additions:
        operations = [{"action": "add_columns", "table": schema["table"], "columns": additions}]
    else:
        operations = []

    return {
        "version": PLAN_VERSION,
        "table": schema["table"],
        "schema_digest": schema_digest(schema),
        "expected_schema": schema,
        "conflicts": conflicts,
        "operations": operations,
    }


def validate_plan(plan: dict[str, Any], schema: dict[str, Any], table: str) -> None:
    if plan.get("version") != PLAN_VERSION or plan.get("table") != table:
        raise GristOpsError("plan version or table does not match this command")
    if plan.get("schema_digest") != schema_digest(schema):
        raise GristOpsError("plan is stale; generate a fresh schema plan")
    expected = build_schema_plan(schema)
    if plan.get("conflicts") != expected["conflicts"] or plan.get("operations") != expected["operations"]:
        raise GristOpsError("plan was edited or is not additive for the current schema")
    if plan.get("conflicts"):
        raise GristOpsError("schema has type conflicts; resolve them manually before applying")


def read_events(path: Path, max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES) -> list[dict[str, Any]]:
    if max_input_bytes <= 0:
        raise GristOpsError("max input bytes must be positive")
    try:
        if path.stat().st_size > max_input_bytes:
            raise GristOpsError(f"event input exceeds {max_input_bytes} bytes")
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GristOpsError(f"could not read {path}: {error}") from error
    try:
        if path.suffix.lower() == ".jsonl":
            events = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            events = json.loads(text)
    except json.JSONDecodeError as error:
        raise GristOpsError(f"invalid event JSON: {error.msg}") from error
    if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
        raise GristOpsError("event input must be a JSON array or JSONL objects")
    if not events:
        raise GristOpsError("event input is empty")
    return events


def event_value(event: dict[str, Any], camel_case: str, snake_case: str) -> Any:
    return event.get(camel_case, event.get(snake_case))


def iso_timestamp(value: Any) -> str:
    if not isinstance(value, str):
        raise GristOpsError("OccurredAt must be an ISO-8601 timestamp string")
    candidate = value.replace("Z", "+00:00")
    try:
        timestamp = dt.datetime.fromisoformat(candidate)
    except ValueError as error:
        raise GristOpsError(f"invalid OccurredAt timestamp: {value}") from error
    if timestamp.tzinfo is None:
        raise GristOpsError("OccurredAt must include a timezone")
    return value


def event_records(
    events: Iterable[dict[str, Any]], source: str | None, environment: str | None
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, event in enumerate(events, start=1):
        event_id = event_value(event, "EventId", "event_id")
        event_type = event_value(event, "EventType", "event_type")
        occurred_at = event_value(event, "OccurredAt", "occurred_at")
        event_source = event_value(event, "Source", "source") or source
        event_environment = event_value(event, "Environment", "environment") or environment
        if not isinstance(event_id, str) or not event_id.strip():
            raise GristOpsError(f"event {index}: EventId must be a non-empty string")
        if event_id in seen_ids:
            raise GristOpsError(f"event {index}: duplicate EventId in one batch")
        if not isinstance(event_type, str) or not event_type.strip():
            raise GristOpsError(f"event {index}: EventType must be a non-empty string")
        if not isinstance(event_source, str) or not event_source.strip():
            raise GristOpsError(f"event {index}: Source is required")
        if not isinstance(event_environment, str) or not event_environment.strip():
            raise GristOpsError(f"event {index}: Environment is required")
        payload = event.get("Payload", event.get("payload", {}))
        try:
            payload_text = canonical_json(payload)
        except (TypeError, ValueError) as error:
            raise GristOpsError(f"event {index}: Payload must be JSON-compatible") from error
        seen_ids.add(event_id)
        records.append(
            {
                "require": {"EventId": event_id},
                "fields": {
                    "OccurredAt": iso_timestamp(occurred_at),
                    "Source": event_source,
                    "Environment": event_environment,
                    "EventType": event_type,
                    "Payload": payload_text,
                },
            }
        )
    return records


def validate_sql(sql: str, args: list[Any]) -> None:
    statement = sql.strip()
    if not READ_ONLY_SQL.match(statement) or ";" in statement or FORBIDDEN_SQL.search(statement):
        raise GristOpsError("query must be one read-only SELECT or WITH statement with no semicolon")
    if not isinstance(args, list) or not all(isinstance(item, (str, int, float)) for item in args):
        raise GristOpsError("query args must be a JSON array of strings or numbers")


def batch_sha256(records: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_json(records).encode("utf-8")).hexdigest()


def verification_suffix(table: str, records: list[dict[str, Any]]) -> str:
    event_ids = [record["require"]["EventId"] for record in records]
    filter_value = quote(canonical_json({"EventId": event_ids}), safe="")
    return f"/tables/{quote(table, safe='')}/records?filter={filter_value}"


def verification_batches(
    client: GristClient, table: str, records: list[dict[str, Any]]
) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for record in records:
        candidate = [*current, record]
        if len(client.path(verification_suffix(table, candidate)).encode("utf-8")) <= MAX_VERIFY_REQUEST_PATH_BYTES:
            current = candidate
            continue
        if not current:
            raise GristOpsError("EventId is too long to verify through the Grist records API")
        batches.append(current)
        current = [record]
        if len(client.path(verification_suffix(table, current)).encode("utf-8")) > MAX_VERIFY_REQUEST_PATH_BYTES:
            raise GristOpsError("EventId is too long to verify through the Grist records API")
    if current:
        batches.append(current)
    return batches


def verify_event_records(
    client: GristClient, table: str, records: list[dict[str, Any]]
) -> dict[str, Any]:
    raw_records: list[Any] = []
    for batch in verification_batches(client, table, records):
        response = client.request("GET", client.path(verification_suffix(table, batch)))
        response_records = response.get("records") if isinstance(response, dict) else None
        if not isinstance(response_records, list):
            raise GristOpsError("Grist returned an invalid records verification response")
        raw_records.extend(response_records)

    found: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw_record in raw_records:
        fields = raw_record.get("fields") if isinstance(raw_record, dict) else None
        event_id = fields.get("EventId") if isinstance(fields, dict) else None
        if isinstance(event_id, str):
            found[event_id].append(fields)

    missing = 0
    duplicate_ids = 0
    mismatched = 0
    for record in records:
        event_id = record["require"]["EventId"]
        matches = found.get(event_id, [])
        if not matches:
            missing += 1
            continue
        if len(matches) != 1:
            duplicate_ids += 1
            continue
        expected = {"EventId": event_id, **record["fields"]}
        actual = {column_id: matches[0].get(column_id) for column_id in EVENT_FIELD_IDS}
        if actual != expected:
            mismatched += 1

    if missing or duplicate_ids or mismatched:
        failures = []
        if missing:
            failures.append(f"{missing} missing")
        if duplicate_ids:
            failures.append(f"{duplicate_ids} duplicate EventId")
        if mismatched:
            failures.append(f"{mismatched} mismatched")
        raise GristOpsError("ingest verification failed: " + ", ".join(failures))
    return {"ok": True, "verified": len(records), "batch_sha256": batch_sha256(records)}


def receipt_for(client: GristClient, table: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    completed_at = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "version": 1,
        "operation": "ingest",
        "completed_at": completed_at,
        "target": {"url": client.settings.url, "doc_id": client.settings.doc_id, "table": table},
        "event_count": len(records),
        "batch_sha256": batch_sha256(records),
    }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    if not path.parent.is_dir():
        raise GristOpsError(f"receipt directory does not exist: {path.parent}")
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_file.write(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    except OSError as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise GristOpsError(f"could not write receipt {path}: {error}") from error


def prepared_event_records(args: argparse.Namespace) -> list[dict[str, Any]]:
    source = args.source or os.environ.get("GRIST_LOG_SOURCE")
    environment = args.environment or os.environ.get("GRIST_LOG_ENVIRONMENT")
    records = event_records(read_events(Path(args.input), args.max_input_bytes), source, environment)
    if len(records) > args.batch_size:
        raise GristOpsError(f"input has {len(records)} events; max batch size is {args.batch_size}")
    return records


def command_doctor(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    tables = client.tables()
    return {
        "ok": True,
        "url": client.settings.url,
        "doc_id": client.settings.doc_id,
        "table_ids": [item.get("id") for item in tables if isinstance(item.get("id"), str)],
    }


def command_plan_schema(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    plan = build_schema_plan(current_schema(client, args.table))
    if args.out:
        output_path = Path(args.out)
        output_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {"ok": True, "plan_path": str(output_path), "operations": plan["operations"], "conflicts": plan["conflicts"]}
    return plan


def command_apply_schema(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    if args.confirm_table != args.table:
        raise GristOpsError("--confirm-table must exactly match --table")
    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GristOpsError(f"could not read schema plan: {error}") from error
    if not isinstance(plan, dict):
        raise GristOpsError("schema plan must be a JSON object")
    schema = current_schema(client, args.table)
    validate_plan(plan, schema, args.table)
    results = []
    for operation in plan["operations"]:
        if operation["action"] == "create_table":
            results.append(client.request("POST", client.path("/tables"), {"tables": [{"id": args.table, "columns": operation["columns"]}]}))
        elif operation["action"] == "add_columns":
            suffix = f"/tables/{quote(args.table, safe='')}/columns"
            results.append(client.request("POST", client.path(suffix), {"columns": operation["columns"]}))
        else:
            raise GristOpsError("unsupported schema operation")
    return {"ok": True, "table": args.table, "applied_operations": len(results)}


def command_ingest(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    records = prepared_event_records(args)
    if args.verify:
        verification_batches(client, args.table, records)
    suffix = f"/tables/{quote(args.table, safe='')}/records?onmany=none&noupdate=true"
    client.request("PUT", client.path(suffix), {"records": records})
    result = {
        "ok": True,
        "table": args.table,
        "upserted": len(records),
        "batch_sha256": batch_sha256(records),
    }
    if args.verify:
        result["verification"] = verify_event_records(client, args.table, records)
    if args.receipt_out:
        write_receipt(Path(args.receipt_out), receipt_for(client, args.table, records))
        result["receipt_path"] = args.receipt_out
    return result


def command_verify_ingest(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    return verify_event_records(client, args.table, prepared_event_records(args))


def command_query(client: GristClient, args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.sql) == bool(args.sql_file):
        raise GristOpsError("provide exactly one of --sql or --sql-file")
    sql = args.sql or Path(args.sql_file).read_text(encoding="utf-8")
    try:
        sql_args = json.loads(args.args_json)
    except json.JSONDecodeError as error:
        raise GristOpsError("--args-json must be valid JSON") from error
    validate_sql(sql, sql_args)
    payload: dict[str, Any] = {"sql": sql.strip(), "args": sql_args}
    if args.timeout is not None:
        if args.timeout <= 0:
            raise GristOpsError("--timeout must be positive")
        payload["timeout"] = args.timeout
    return client.request("POST", client.path("/sql"), payload)


def command_mcp_info(args: argparse.Namespace) -> dict[str, Any]:
    full = args.edition == "full"
    return {
        "edition": args.edition,
        "built_in_mcp": full,
        "endpoint": "https://<grist-host>/api/mcp" if full else None,
        "required_environment": (
            ["GRIST_MCP_ENABLED=true", "GRIST_ENABLE_OIDC_SERVER=true", "GRIST_OIDC_CIMD_ALLOWED_HOSTS=<trusted client hosts>"]
            if full
            else []
        ),
        "guidance": (
            "Enable only after approving the persistent instance change and limit CIMD hosts."
            if full
            else "Use REST plus read-only SQL. Built-in self-hosted MCP requires Full edition."
        ),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--url", help="Grist base URL; defaults to GRIST_URL")
    result.add_argument("--doc-id", help="Grist document ID; defaults to GRIST_DOC_ID")
    result.add_argument("--token", help="API key or OAuth token; defaults to GRIST_TOKEN")
    result.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    commands = result.add_subparsers(dest="command", required=True)

    commands.add_parser("doctor", help="verify authenticated document access")
    plan = commands.add_parser("plan-schema", help="generate an additive AppEvents schema plan")
    plan.add_argument("--table", default=DEFAULT_TABLE)
    plan.add_argument("--out", help="write the plan to this path instead of stdout")
    apply = commands.add_parser("apply-schema", help="apply an approved schema plan")
    apply.add_argument("--table", default=DEFAULT_TABLE)
    apply.add_argument("--plan", required=True)
    apply.add_argument("--confirm-table", required=True)
    def add_event_input_arguments(command: argparse.ArgumentParser) -> None:
        command.add_argument("--table", default=DEFAULT_TABLE)
        command.add_argument("--input", required=True)
        command.add_argument("--source")
        command.add_argument("--environment")
        command.add_argument("--batch-size", type=int, default=100)
        command.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_INPUT_BYTES)

    ingest = commands.add_parser("ingest", help="validate and upsert one event batch")
    add_event_input_arguments(ingest)
    ingest.add_argument("--verify", action="store_true", help="verify the rows after upsert")
    ingest.add_argument("--receipt-out", help="write a payload-free receipt after success")
    verify = commands.add_parser("verify-ingest", help="verify one event batch is stored exactly once")
    add_event_input_arguments(verify)
    query = commands.add_parser("query", help="run one parameterized read-only SQL query")
    query.add_argument("--sql")
    query.add_argument("--sql-file")
    query.add_argument("--args-json", default="[]")
    query.add_argument("--timeout", type=int, help="optional timeout in milliseconds")
    mcp = commands.add_parser("mcp-info", help="show the supported MCP path")
    mcp.add_argument("--edition", choices=("community", "full", "unknown"), default="unknown")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "mcp-info":
            output = command_mcp_info(args)
        else:
            client = GristClient(Settings.from_args(args))
            handlers = {
                "doctor": command_doctor,
                "plan-schema": command_plan_schema,
                "apply-schema": command_apply_schema,
                "ingest": command_ingest,
                "verify-ingest": command_verify_ingest,
                "query": command_query,
            }
            output = handlers[args.command](client, args)
        write_result(output, args.pretty)
        return 0
    except GristOpsError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
