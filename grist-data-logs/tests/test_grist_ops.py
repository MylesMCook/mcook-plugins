from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "grist_ops.py"
SPEC = importlib.util.spec_from_file_location("grist_ops", MODULE_PATH)
assert SPEC and SPEC.loader
grist_ops = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = grist_ops
SPEC.loader.exec_module(grist_ops)


class FakeClient:
    def __init__(self, exists: bool = False, records_response=None, records_responses=None) -> None:
        self.exists = exists
        self.requests = []
        self.settings = SimpleNamespace(url="https://grist.example", doc_id="document")
        self.records_response = records_response
        self.records_responses = list(records_responses or [])

    def path(self, suffix: str) -> str:
        return f"/api/docs/document{suffix}"

    def tables(self):
        return [{"id": "AppEvents"}] if self.exists else []

    def columns(self, table: str):
        return []

    def request(self, method: str, path: str, payload=None):
        self.requests.append((method, path, payload))
        if method == "GET" and "/records?filter=" in path:
            if self.records_responses:
                return self.records_responses.pop(0)
            if self.records_response is not None:
                return self.records_response
        return {"ok": True}


class GristOpsTests(unittest.TestCase):
    def test_expected_schema_creates_missing_table(self) -> None:
        plan = grist_ops.build_schema_plan({"table": "AppEvents", "exists": False, "columns": {}})
        self.assertEqual(plan["operations"][0]["action"], "create_table")
        self.assertEqual(len(plan["operations"][0]["columns"]), 6)

    def test_expected_schema_adds_only_missing_columns(self) -> None:
        schema = {"table": "AppEvents", "exists": True, "columns": {"EventId": "Text", "OccurredAt": "Text"}}
        plan = grist_ops.build_schema_plan(schema)
        additions = plan["operations"][0]["columns"]
        self.assertEqual([column["id"] for column in additions], ["Source", "Environment", "EventType", "Payload"])

    def test_schema_conflict_is_not_an_operation(self) -> None:
        schema = {"table": "AppEvents", "exists": True, "columns": {"EventId": "Int"}}
        plan = grist_ops.build_schema_plan(schema)
        self.assertEqual(plan["operations"], [])
        self.assertEqual(plan["conflicts"][0]["column"], "EventId")

    def test_plan_validation_rejects_edit(self) -> None:
        schema = {"table": "AppEvents", "exists": False, "columns": {}}
        plan = grist_ops.build_schema_plan(schema)
        plan["operations"] = []
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.validate_plan(plan, schema, "AppEvents")

    def test_plan_validation_rejects_stale_schema(self) -> None:
        before = {"table": "AppEvents", "exists": False, "columns": {}}
        after = {"table": "AppEvents", "exists": True, "columns": {}}
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.validate_plan(grist_ops.build_schema_plan(before), after, "AppEvents")

    def test_event_records_normalizes_a_json_payload(self) -> None:
        records = grist_ops.event_records(
            [{"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed", "payload": {"b": 2, "a": 1}}],
            "app",
            "production",
        )
        self.assertEqual(records[0]["require"], {"EventId": "event-1"})
        self.assertEqual(records[0]["fields"]["Payload"], '{"a":1,"b":2}')

    def test_event_records_preserve_timestamp_text_for_replay(self) -> None:
        records = grist_ops.event_records(
            [{"event_id": "event-1", "occurred_at": "2026-07-10T10:04:05-05:00", "event_type": "run.completed"}],
            "app",
            "production",
        )
        self.assertEqual(records[0]["fields"]["OccurredAt"], "2026-07-10T10:04:05-05:00")

    def test_event_records_require_a_timezone(self) -> None:
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.event_records(
                [{"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05", "event_type": "run.completed"}],
                "app",
                "production",
            )

    def test_event_records_reject_duplicate_ids(self) -> None:
        event = {"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.event_records([event, event], "app", "production")

    def test_read_events_accepts_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text('{"event_id":"one"}\n{"event_id":"two"}\n', encoding="utf-8")
            self.assertEqual(len(grist_ops.read_events(path)), 2)

    def test_read_events_rejects_non_array_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            path.write_text(json.dumps({"event_id": "one"}), encoding="utf-8")
            with self.assertRaises(grist_ops.GristOpsError):
                grist_ops.read_events(path)

    def test_read_events_rejects_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            path.write_text("{not valid json", encoding="utf-8")
            with self.assertRaises(grist_ops.GristOpsError):
                grist_ops.read_events(path)

    def test_read_events_enforces_byte_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(grist_ops.GristOpsError):
                grist_ops.read_events(path, max_input_bytes=1)

    def test_query_validation_allows_parameterized_select(self) -> None:
        grist_ops.validate_sql("SELECT * FROM AppEvents WHERE EventType = ?", ["run.completed"])

    def test_query_validation_rejects_mutation_and_semicolon(self) -> None:
        for sql in (
            "DELETE FROM AppEvents",
            "SELECT * FROM AppEvents;",
            "WITH current AS (SELECT 1) DELETE FROM AppEvents",
        ):
            with self.assertRaises(grist_ops.GristOpsError):
                grist_ops.validate_sql(sql, [])

    def test_mcp_info_does_not_claim_community_support(self) -> None:
        args = type("Args", (), {"edition": "community"})()
        self.assertFalse(grist_ops.command_mcp_info(args)["built_in_mcp"])

    def test_settings_rejects_non_loopback_http(self) -> None:
        args = SimpleNamespace(url="http://grist.example", doc_id="document", token="token")
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.Settings.from_args(args)

    def test_settings_allows_loopback_http(self) -> None:
        args = SimpleNamespace(url="http://127.0.0.1:8484", doc_id="document", token="token")
        self.assertEqual(grist_ops.Settings.from_args(args).url, "http://127.0.0.1:8484")

    def test_apply_schema_posts_a_complete_missing_table(self) -> None:
        client = FakeClient()
        schema = {"table": "AppEvents", "exists": False, "columns": {}}
        plan = grist_ops.build_schema_plan(schema)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            args = SimpleNamespace(table="AppEvents", confirm_table="AppEvents", plan=str(path))
            result = grist_ops.command_apply_schema(client, args)
        self.assertEqual(result["applied_operations"], 1)
        self.assertEqual(client.requests[0][0:2], ("POST", "/api/docs/document/tables"))
        self.assertEqual(client.requests[0][2]["tables"][0]["id"], "AppEvents")

    def test_ingest_uses_record_upsert_with_event_id_requirements(self) -> None:
        client = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            path.write_text(json.dumps([{"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}]), encoding="utf-8")
            args = SimpleNamespace(
                input=str(path), source="app", environment="test", batch_size=100, max_input_bytes=1_000_000,
                table="AppEvents", verify=False, receipt_out=None,
            )
            result = grist_ops.command_ingest(client, args)
        self.assertEqual(result["upserted"], 1)
        self.assertIn("batch_sha256", result)
        self.assertEqual(client.requests[0][0:2], ("PUT", "/api/docs/document/tables/AppEvents/records?onmany=none&noupdate=true"))
        self.assertEqual(client.requests[0][2]["records"][0]["require"], {"EventId": "event-1"})

    def test_ingest_writes_a_payload_free_receipt(self) -> None:
        client = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            events_path = Path(directory) / "events.json"
            receipt_path = Path(directory) / "receipt.json"
            events_path.write_text(json.dumps([{"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed", "payload": {"private": "value"}}]), encoding="utf-8")
            args = SimpleNamespace(
                input=str(events_path), source="app", environment="test", batch_size=100, max_input_bytes=1_000_000,
                table="AppEvents", verify=False, receipt_out=str(receipt_path),
            )
            grist_ops.command_ingest(client, args)
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["event_count"], 1)
        self.assertNotIn("payload", json.dumps(receipt).lower())
        self.assertIn("batch_sha256", receipt)

    def test_verify_ingest_accepts_one_matching_row_per_event(self) -> None:
        event = {"event_id": "event-1", "occurred_at": "2026-07-10T10:04:05-05:00", "event_type": "run.completed", "payload": {"a": 1}}
        records = grist_ops.event_records([event], "app", "test")
        fields = {"EventId": "event-1", **records[0]["fields"]}
        client = FakeClient(records_response={"records": [{"fields": fields}]})
        result = grist_ops.verify_event_records(client, "AppEvents", records)
        self.assertEqual(result["verified"], 1)
        self.assertEqual(client.requests[0][0], "GET")
        self.assertIn("/api/docs/document/tables/AppEvents/records?filter=", client.requests[0][1])

    def test_verify_ingest_rejects_a_reused_event_id(self) -> None:
        event = {"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}
        records = grist_ops.event_records([event], "app", "test")
        fields = {"EventId": "event-1", **records[0]["fields"]}
        client = FakeClient(records_response={"records": [{"fields": fields}, {"fields": fields}]})
        with self.assertRaises(grist_ops.GristOpsError):
            grist_ops.verify_event_records(client, "AppEvents", records)

    def test_verify_ingest_reports_missing_and_mismatched_rows(self) -> None:
        events = [
            {"event_id": "missing", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"},
            {"event_id": "mismatched", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"},
        ]
        records = grist_ops.event_records(events, "app", "test")
        mismatched_fields = {"EventId": "mismatched", **records[1]["fields"], "EventType": "run.failed"}
        client = FakeClient(records_response={"records": [{"fields": mismatched_fields}]})
        with self.assertRaisesRegex(grist_ops.GristOpsError, "1 missing, 1 mismatched"):
            grist_ops.verify_event_records(client, "AppEvents", records)

    def test_verification_chunks_long_batches_before_writing(self) -> None:
        events = [
            {"event_id": "event-one", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"},
            {"event_id": "event-two", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"},
        ]
        records = grist_ops.event_records(events, "app", "test")
        fields = [{"fields": {"EventId": record["require"]["EventId"], **record["fields"]}} for record in records]
        original_limit = grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES
        grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES = 100
        try:
            client = FakeClient(records_responses=[{"records": [fields[0]]}, {"records": [fields[1]]}])
            result = grist_ops.verify_event_records(client, "AppEvents", records)
        finally:
            grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES = original_limit
        self.assertEqual(result["verified"], 2)
        self.assertEqual([request[0] for request in client.requests], ["GET", "GET"])

    def test_ingest_rejects_unverifiable_id_before_upsert(self) -> None:
        client = FakeClient()
        event = {"event_id": "x" * 500, "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}
        original_limit = grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES
        grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES = 100
        try:
            with tempfile.TemporaryDirectory() as directory:
                events_path = Path(directory) / "events.json"
                events_path.write_text(json.dumps([event]), encoding="utf-8")
                args = SimpleNamespace(
                    input=str(events_path), source="app", environment="test", batch_size=100,
                    max_input_bytes=1_000_000, table="AppEvents", verify=True, receipt_out=None,
                )
                with self.assertRaises(grist_ops.GristOpsError):
                    grist_ops.command_ingest(client, args)
        finally:
            grist_ops.MAX_VERIFY_REQUEST_PATH_BYTES = original_limit
        self.assertEqual(client.requests, [])

    def test_ingest_verifies_then_writes_matching_receipt(self) -> None:
        event = {"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}
        expected_records = grist_ops.event_records([event], "app", "test")
        fields = {"EventId": "event-1", **expected_records[0]["fields"]}
        client = FakeClient(records_response={"records": [{"fields": fields}]})
        with tempfile.TemporaryDirectory() as directory:
            events_path = Path(directory) / "events.json"
            receipt_path = Path(directory) / "receipt.json"
            events_path.write_text(json.dumps([event]), encoding="utf-8")
            args = SimpleNamespace(
                input=str(events_path), source="app", environment="test", batch_size=100,
                max_input_bytes=1_000_000, table="AppEvents", verify=True,
                receipt_out=str(receipt_path),
            )
            result = grist_ops.command_ingest(client, args)
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual([request[0] for request in client.requests], ["PUT", "GET"])
        self.assertEqual(result["verification"]["batch_sha256"], result["batch_sha256"])
        self.assertEqual(receipt["batch_sha256"], result["batch_sha256"])
        self.assertEqual(result["receipt_path"], str(receipt_path))

    def test_ingest_collision_preserves_row_and_writes_no_receipt(self) -> None:
        event = {"event_id": "event-1", "occurred_at": "2026-07-10T15:04:05Z", "event_type": "run.completed"}
        old_fields = {
            "EventId": "event-1",
            "OccurredAt": "2026-07-10T15:04:04Z",
            "Source": "app",
            "Environment": "test",
            "EventType": "run.completed",
            "Payload": "{}",
        }
        client = FakeClient(records_response={"records": [{"fields": old_fields}]})
        with tempfile.TemporaryDirectory() as directory:
            events_path = Path(directory) / "events.json"
            receipt_path = Path(directory) / "receipt.json"
            events_path.write_text(json.dumps([event]), encoding="utf-8")
            args = SimpleNamespace(
                input=str(events_path), source="app", environment="test", batch_size=100,
                max_input_bytes=1_000_000, table="AppEvents", verify=True,
                receipt_out=str(receipt_path),
            )
            with self.assertRaisesRegex(grist_ops.GristOpsError, "1 mismatched"):
                grist_ops.command_ingest(client, args)
            self.assertFalse(receipt_path.exists())
        self.assertIn("noupdate=true", client.requests[0][1])

    def test_query_omits_timeout_unless_the_user_sets_one(self) -> None:
        client = FakeClient()
        args = SimpleNamespace(sql="SELECT * FROM AppEvents", sql_file=None, args_json="[]", timeout=None)
        grist_ops.command_query(client, args)
        self.assertNotIn("timeout", client.requests[0][2])


if __name__ == "__main__":
    unittest.main()
