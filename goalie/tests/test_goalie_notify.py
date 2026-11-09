#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "hooks" / "goalie_notify.py"
HOOKS_PATH = Path(__file__).resolve().parents[1] / "hooks" / "hooks.json"
SPEC = importlib.util.spec_from_file_location("goalie_notify", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
goalie_notify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(goalie_notify)
TEST_WEBHOOK_URL = "https://api.brrr.now/v1/" + "br_test"
DEFAULT_CODEX_IMAGE_URL = (
    "https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/"
    "packages/static-png/light/codex-color.png"
)


class GoalieNotifyTests(unittest.TestCase):
    def test_hook_commands_are_cross_platform(self):
        hooks = json.loads(HOOKS_PATH.read_text(encoding="utf-8"))
        command = hooks["hooks"]["Stop"][0]["hooks"][0]

        self.assertEqual(
            command["command"],
            'python3 "${PLUGIN_ROOT}/hooks/goalie_notify.py"',
        )
        self.assertEqual(
            command["commandWindows"],
            'py -3 "%PLUGIN_ROOT%\\hooks\\goalie_notify.py"',
        )

    def run_hook(self, payload, env=None):
        sent = []

        def post_json(url, body):
            sent.append((url, body))

        stderr = io.StringIO()
        code = goalie_notify.main(
            stdin=io.StringIO(json.dumps(payload)),
            env=env if env is not None else {"BRRR_WEBHOOK_URL": TEST_WEBHOOK_URL},
            post_json=post_json,
            stderr=stderr,
        )
        return code, sent, stderr.getvalue()

    def write_goal_transcript(self, tmpdir):
        transcript = Path(tmpdir) / "session.jsonl"
        transcript.write_text(
            json.dumps(
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "get_goal",
                        "arguments": "{}",
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return transcript

    def test_blocked_goal_transcript_sends_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "session.jsonl"
            transcript.write_text(
                json.dumps(
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "name": "update_goal",
                            "arguments": "{\"status\":\"blocked\"}",
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            code, sent, stderr = self.run_hook(
                {
                    "cwd": "/tmp/example",
                    "transcript_path": str(transcript),
                    "last_assistant_message": "I cannot make more progress.",
                }
            )

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0][0], TEST_WEBHOOK_URL)
        self.assertEqual(sent[0][1]["title"], "Goal blocked")
        self.assertEqual(sent[0][1]["subtitle"], "example")
        self.assertIn("blocked", sent[0][1]["message"])
        self.assertEqual(sent[0][1]["thread_id"], "codex-goalie-example-blocked")
        self.assertEqual(sent[0][1]["sound"], "brrr")
        self.assertEqual(sent[0][1]["interruption_level"], "time-sensitive")
        self.assertEqual(sent[0][1]["open_url"], "chatgpt://")
        self.assertEqual(sent[0][1]["image_url"], DEFAULT_CODEX_IMAGE_URL)
        self.assertIn("expiration_date", sent[0][1])

    def test_manual_checkpoint_message_sends_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = self.write_goal_transcript(tmpdir)
            code, sent, stderr = self.run_hook(
                {
                    "cwd": "/tmp/project",
                    "transcript_path": str(transcript),
                    "last_assistant_message": "Manual checkpoint: open Xcode and choose your signing team.",
                }
            )

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0][1]["title"], "Manual checkpoint")
        self.assertEqual(sent[0][1]["subtitle"], "project")
        self.assertIn("Manual checkpoint", sent[0][1]["message"])
        self.assertEqual(sent[0][1]["thread_id"], "codex-goalie-project-manual")
        self.assertEqual(sent[0][1]["open_url"], "chatgpt://")

    def test_normal_chat_manual_checkpoint_sends_nothing(self):
        code, sent, stderr = self.run_hook(
            {
                "cwd": "/tmp/project",
                "last_assistant_message": "Manual checkpoint: this is not in a Goal run.",
            }
        )

        self.assertEqual(code, 0)
        self.assertEqual(sent, [])
        self.assertEqual(stderr, "")

    def test_open_url_can_be_overridden(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = self.write_goal_transcript(tmpdir)
            code, sent, stderr = self.run_hook(
                {
                    "cwd": "/tmp/project",
                    "transcript_path": str(transcript),
                    "last_assistant_message": "Manual checkpoint: approve the device prompt.",
                },
                env={
                    "BRRR_WEBHOOK_URL": TEST_WEBHOOK_URL,
                    "GOALIE_OPEN_URL": "https://chatgpt.com/",
                    "GOALIE_IMAGE_URL": "https://example.com/codex.png",
                    "GOALIE_SOUND": "upbeat_bells",
                    "GOALIE_INTERRUPTION_LEVEL": "active",
                    "GOALIE_FILTER_CRITERIA": "work",
                },
            )

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(sent[0][1]["open_url"], "https://chatgpt.com/")
        self.assertEqual(sent[0][1]["image_url"], "https://example.com/codex.png")
        self.assertEqual(sent[0][1]["sound"], "upbeat_bells")
        self.assertEqual(sent[0][1]["interruption_level"], "active")
        self.assertEqual(sent[0][1]["filter_criteria"], "work")

    def test_normal_completion_sends_nothing(self):
        code, sent, stderr = self.run_hook(
            {
                "cwd": "/tmp/project",
                "last_assistant_message": "Implemented the change and ran the tests.",
            }
        )

        self.assertEqual(code, 0)
        self.assertEqual(sent, [])
        self.assertEqual(stderr, "")

    def test_missing_webhook_exits_cleanly(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = self.write_goal_transcript(tmpdir)
            code, sent, stderr = self.run_hook(
                {
                    "cwd": "/tmp/project",
                    "transcript_path": str(transcript),
                    "last_assistant_message": "Manual checkpoint: approve the device prompt.",
                },
                env={},
            )

        self.assertEqual(code, 0)
        self.assertEqual(sent, [])
        self.assertIn("BRRR_WEBHOOK_URL is not set", stderr)

    def test_invalid_webhook_exits_cleanly(self):
        code, sent, stderr = self.run_hook(
            {
                "cwd": "/tmp/project",
                "last_assistant_message": "Goal is blocked by missing credentials.",
            },
            env={"BRRR_WEBHOOK_URL": "https://example.com/nope"},
        )

        self.assertEqual(code, 0)
        self.assertEqual(sent, [])
        self.assertIn("not a brrr webhook URL", stderr)


if __name__ == "__main__":
    unittest.main()
