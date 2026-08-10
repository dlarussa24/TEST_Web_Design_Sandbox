#!/usr/bin/env python3
"""Remind the assistant to report a metered MCP's remaining balance.

Shell scripts cannot call MCP tools -- the connectors are authenticated by
claude.ai server-side and no token reaches this container's environment. So
this hook cannot fetch a balance itself. What it can do is fire at exactly
the moment a metered server is used and inject an instruction naming the
reader tool to call, which is the deterministic half of the job.

Two events:
  PostToolUse       -- a metered tool ran; emit the reminder (once per turn
                       per server).
  UserPromptSubmit  -- a new turn started; clear the per-turn markers.
"""

import json
import os
import sys
import tempfile

# server -> (reader tool, how to phrase the figures)
METERED = {
    "Higgsfield": (
        "mcp__Higgsfield__balance",
        "returns {credits, subscription_plan_type}. That is a remaining "
        "balance with no denominator, so report remaining credits and the "
        "plan; do not invent a plan total.",
    ),
    "Cloudinary": (
        "mcp__Cloudinary__get-usage-details",
        "returns credits.usage / credits.limit / credits.used_percent. "
        "Report used/total and remaining as limit - usage.",
    ),
    "Lovable": (
        "mcp__Lovable__get_workspace",
        "documents a credit balance field but omitted it for the free "
        "workspace when last checked. If it is still absent, say so rather "
        "than reporting zero.",
    ),
    "Netlify": (
        None,
        "has no billing, quota, or usage field on any exposed tool, and "
        "there is no NETLIFY_AUTH_TOKEN or CLI here to reach the REST API. "
        "State that the figures are unavailable and name that reason.",
    ),
}

# Reader tools must not re-arm the reminder, or every balance check loops.
READERS = {r for r, _ in METERED.values() if r}


def marker_dir(session_id):
    d = os.path.join(tempfile.gettempdir(), "mcp-balance-" + (session_id or "nosession"))
    os.makedirs(d, exist_ok=True)
    return d


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    event = data.get("hook_event_name")
    session = data.get("session_id", "")

    if event == "UserPromptSubmit":
        # New turn: forget which servers were already reported on.
        d = marker_dir(session)
        for name in os.listdir(d):
            try:
                os.remove(os.path.join(d, name))
            except OSError:
                pass
        return 0

    tool = data.get("tool_name", "")
    if not tool.startswith("mcp__") or tool in READERS:
        return 0

    server = tool.split("__")[1] if len(tool.split("__")) > 1 else ""
    if server not in METERED:
        return 0

    marker = os.path.join(marker_dir(session), server)
    if os.path.exists(marker):
        return 0
    open(marker, "w").close()

    reader, note = METERED[server]
    if reader:
        msg = (
            f"This turn used the metered {server} MCP. Before you finish, call "
            f"{reader} and report the balance at the end of your response: "
            f"used/total and remaining. {reader} {note} Report the real numbers "
            f"only -- never estimate or infer them."
        )
    else:
        msg = (
            f"This turn used the metered {server} MCP, whose balance is not "
            f"readable here: {server} {note}"
        )

    json.dump(
        {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}},
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
