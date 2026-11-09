#!/usr/bin/env python3
"""Send a quiet brrr notification when a Codex Goal appears blocked."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, NamedTuple, TextIO


WEBHOOK_ENV = "BRRR_WEBHOOK_URL"
OPEN_URL_ENV = "GOALIE_OPEN_URL"
SOUND_ENV = "GOALIE_SOUND"
INTERRUPTION_LEVEL_ENV = "GOALIE_INTERRUPTION_LEVEL"
FILTER_CRITERIA_ENV = "GOALIE_FILTER_CRITERIA"
IMAGE_URL_ENV = "GOALIE_IMAGE_URL"
THREAD_PREFIX_ENV = "GOALIE_THREAD_PREFIX"
EXPIRATION_MINUTES_ENV = "GOALIE_EXPIRATION_MINUTES"
DEFAULT_OPEN_URL = "chatgpt://"
DEFAULT_IMAGE_URL = (
    "https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/"
    "packages/static-png/light/codex-color.png"
)
DEFAULT_SOUND = "brrr"
DEFAULT_INTERRUPTION_LEVEL = "time-sensitive"
DEFAULT_THREAD_PREFIX = "codex-goalie"
DEFAULT_EXPIRATION_MINUTES = 360
MAX_TRANSCRIPT_BYTES = 512_000
MAX_MESSAGE_CHARS = 360
ALLOWED_HOSTS = {"api.brrr.now", "dev.api.brrr.now"}
WEBHOOK_PATH_RE = re.compile(r"^/v1/br_[A-Za-z0-9_]+$")
VALID_INTERRUPTION_LEVELS = {"passive", "active", "time-sensitive", "critical"}
GOAL_TOOL_NAMES = {"create_goal", "get_goal", "update_goal"}


class Attention(NamedTuple):
    title: str
    message: str
    kind: str


def main(
    stdin: TextIO | None = None,
    env: dict[str, str] | None = None,
    post_json: Callable[[str, dict[str, str]], None] | None = None,
    stderr: TextIO | None = None,
) -> int:
    stdin = stdin or sys.stdin
    env = env if env is not None else os.environ
    post_json = post_json or send_webhook
    stderr = stderr or sys.stderr

    try:
        hook_input = json.load(stdin)
    except Exception as exc:
        print(f"goalie notify skipped: invalid hook input: {exc}", file=stderr)
        return 0

    if not isinstance(hook_input, dict):
        print("goalie notify skipped: hook input was not an object", file=stderr)
        return 0

    attention = classify_attention(hook_input)
    if attention is None:
        return 0

    webhook_url = env.get(WEBHOOK_ENV, "").strip()
    if not webhook_url:
        print(f"goalie notify skipped: {WEBHOOK_ENV} is not set", file=stderr)
        return 0
    if not is_allowed_brrr_webhook(webhook_url):
        print(f"goalie notify skipped: {WEBHOOK_ENV} is not a brrr webhook URL", file=stderr)
        return 0

    payload = build_payload(hook_input, attention, env)
    try:
        post_json(webhook_url, payload)
    except Exception as exc:
        print(f"goalie notify failed: {exc}", file=stderr)
    return 0


def classify_attention(hook_input: dict[str, Any]) -> Attention | None:
    transcript_path = read_string(hook_input, "transcript_path")
    if transcript_path and transcript_has_blocked_goal(transcript_path):
        return Attention("Goal blocked", "Goal was marked blocked.", "blocked")

    message = read_string(hook_input, "last_assistant_message") or ""
    attention = extract_attention(message)
    if attention is None:
        return None
    if is_goal_scoped_attention(message, transcript_path):
        return attention
    return None


def transcript_has_blocked_goal(transcript_path: str) -> bool:
    path = Path(transcript_path).expanduser()
    try:
        data = read_tail(path, MAX_TRANSCRIPT_BYTES)
    except OSError:
        return False

    for raw_line in reversed(data.splitlines()):
        line = raw_line.strip()
        if not line or "update_goal" not in line or "blocked" not in line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event_contains_blocked_goal(event):
            return True
    return False


def transcript_has_goal_activity(transcript_path: str) -> bool:
    path = Path(transcript_path).expanduser()
    try:
        data = read_tail(path, MAX_TRANSCRIPT_BYTES)
    except OSError:
        return False

    for raw_line in reversed(data.splitlines()):
        line = raw_line.strip()
        if not line or not any(name in line for name in GOAL_TOOL_NAMES):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event_contains_goal_tool(event):
            return True
    return False


def event_contains_blocked_goal(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("name") == "update_goal" and arguments_are_blocked(value.get("arguments")):
            return True
        return any(event_contains_blocked_goal(item) for item in value.values())
    if isinstance(value, list):
        return any(event_contains_blocked_goal(item) for item in value)
    return False


def event_contains_goal_tool(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("name") in GOAL_TOOL_NAMES:
            return True
        return any(event_contains_goal_tool(item) for item in value.values())
    if isinstance(value, list):
        return any(event_contains_goal_tool(item) for item in value)
    return False


def arguments_are_blocked(arguments: Any) -> bool:
    if isinstance(arguments, dict):
        return arguments.get("status") == "blocked"
    if isinstance(arguments, str):
        try:
            parsed = json.loads(arguments)
        except json.JSONDecodeError:
            return "blocked" in arguments and "status" in arguments
        return isinstance(parsed, dict) and parsed.get("status") == "blocked"
    return False


def extract_attention(message: str) -> Attention | None:
    normalized = " ".join(message.lower().split())
    if not normalized:
        return None

    negative_patterns = (
        "no blocker",
        "no remaining blocker",
        "not blocked",
        "unblocked",
        "remaining blocker: none",
        "remaining blockers: none",
    )
    if any(pattern in normalized for pattern in negative_patterns):
        return None

    line = first_relevant_line(message)
    checks = (
        ("manual checkpoint", "Manual checkpoint", "Manual checkpoint needs attention.", "manual"),
        ("needs your input", "Codex needs input", "Codex is waiting for input.", "input"),
        ("need your input", "Codex needs input", "Codex is waiting for input.", "input"),
        ("waiting on you", "Codex needs input", "Codex is waiting for input.", "input"),
        ("cannot proceed", "Codex cannot proceed", "Codex cannot proceed.", "blocked"),
        ("can't proceed", "Codex cannot proceed", "Codex cannot proceed.", "blocked"),
        ("unable to proceed", "Codex cannot proceed", "Codex cannot proceed.", "blocked"),
        ("goal is blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("goal blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("i'm blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("i am blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("we're blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("we are blocked", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("blocked by", "Goal blocked", "Goal appears blocked.", "blocked"),
        ("remaining blocker", "Remaining blocker", "A remaining blocker needs attention.", "blocked"),
    )
    for pattern, title, fallback, kind in checks:
        if pattern in normalized:
            return Attention(title, line or fallback, kind)
    return None


def is_goal_scoped_attention(message: str, transcript_path: str | None) -> bool:
    if transcript_path and transcript_has_goal_activity(transcript_path):
        return True
    return message_explicitly_mentions_goal_status(message)


def message_explicitly_mentions_goal_status(message: str) -> bool:
    normalized = " ".join(message.lower().split())
    return any(
        pattern in normalized
        for pattern in (
            "goal is blocked",
            "goal blocked",
            "goal appears blocked",
            "goal was marked blocked",
            "goal needs input",
            "goal needs your input",
            "goal manual checkpoint",
            "goal checkpoint",
        )
    )


def first_relevant_line(message: str) -> str | None:
    patterns = (
        "manual checkpoint",
        "needs your input",
        "need your input",
        "waiting on you",
        "cannot proceed",
        "can't proceed",
        "unable to proceed",
        "goal is blocked",
        "goal blocked",
        "blocked by",
        "remaining blocker",
    )
    for raw_line in message.splitlines():
        cleaned = clean_summary(raw_line)
        lower = cleaned.lower()
        if cleaned and any(pattern in lower for pattern in patterns):
            return cleaned
    return None


def build_payload(
    hook_input: dict[str, Any],
    attention: Attention,
    env: dict[str, str],
) -> dict[str, str]:
    cwd = read_string(hook_input, "cwd")
    project = Path(cwd).name if cwd else "Codex"
    message = clean_summary(attention.message) or "Codex needs attention."
    payload = {
        "title": attention.title,
        "subtitle": project,
        "message": truncate(message, MAX_MESSAGE_CHARS),
        "thread_id": build_thread_id(project, attention.kind, env),
    }
    add_optional_payload_field(payload, "sound", env.get(SOUND_ENV, DEFAULT_SOUND))
    add_optional_payload_field(payload, "open_url", env.get(OPEN_URL_ENV, DEFAULT_OPEN_URL))
    add_optional_payload_field(payload, "image_url", env.get(IMAGE_URL_ENV, DEFAULT_IMAGE_URL))
    add_optional_payload_field(payload, "filter_criteria", env.get(FILTER_CRITERIA_ENV))

    interruption_level = normalize_interruption_level(
        env.get(INTERRUPTION_LEVEL_ENV, DEFAULT_INTERRUPTION_LEVEL)
    )
    add_optional_payload_field(payload, "interruption_level", interruption_level)

    expiration_date = build_expiration_date(env.get(EXPIRATION_MINUTES_ENV))
    add_optional_payload_field(payload, "expiration_date", expiration_date)
    return payload


def add_optional_payload_field(payload: dict[str, str], key: str, value: str | None) -> None:
    if value and value.strip():
        payload[key] = value.strip()


def build_thread_id(project: str, kind: str, env: dict[str, str]) -> str:
    prefix = env.get(THREAD_PREFIX_ENV, DEFAULT_THREAD_PREFIX).strip() or DEFAULT_THREAD_PREFIX
    return f"{slugify(prefix)}-{slugify(project)}-{slugify(kind)}"


def normalize_interruption_level(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip().lower()
    if normalized in {"", "none", "off"}:
        return None
    return normalized if normalized in VALID_INTERRUPTION_LEVELS else DEFAULT_INTERRUPTION_LEVEL


def build_expiration_date(value: str | None) -> str | None:
    raw_value = (value or "").strip().lower()
    if raw_value in {"none", "off", "0"}:
        return None
    try:
        minutes = int(raw_value) if raw_value else DEFAULT_EXPIRATION_MINUTES
    except ValueError:
        minutes = DEFAULT_EXPIRATION_MINUTES
    minutes = min(max(minutes, 1), 24 * 60)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return expires_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48].strip("-") or "codex"


def send_webhook(webhook_url: str, payload: dict[str, str]) -> None:
    request = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "user-agent": "goalie-codex-hook/0.1.0",
            "content-type": "application/json",
            "accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=2) as response:
        body = response.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {}
        if response.status != 202 or parsed.get("success") is not True:
            error = parsed.get("error") if isinstance(parsed, dict) else None
            raise RuntimeError(error or f"unexpected response status {response.status}")


def is_allowed_brrr_webhook(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and parsed.hostname in ALLOWED_HOSTS
        and bool(WEBHOOK_PATH_RE.fullmatch(parsed.path))
    )


def read_tail(path: Path, max_bytes: int) -> str:
    size = path.stat().st_size
    with path.open("rb") as handle:
        if size > max_bytes:
            handle.seek(size - max_bytes)
        return handle.read().decode("utf-8", errors="replace")


def clean_summary(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"^[#>*\-\s]+", "", cleaned)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return truncate(cleaned, MAX_MESSAGE_CHARS)


def truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def read_string(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    return value if isinstance(value, str) and value.strip() else None


if __name__ == "__main__":
    raise SystemExit(main())
