#!/usr/bin/env python3
"""Probe Netlify account quotas and print only the figures.

This runs on a GitHub runner because api.netlify.com is blocked by the
sandbox's egress policy, and it reads the token from an Actions secret so
the credential never enters the sandbox or a settings field.

IMPORTANT: this repository is public, so Actions logs are public. The raw
API response is never printed. Numbers and booleans are safe to publish and
are printed in full; string values are redacted unless the key is on a small
allowlist of non-identifying fields (plan tier, unit, period). That is enough
to learn the response shape without publishing account names, emails, slugs
or IDs.
"""

import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.netlify.com/api/v1/accounts"

# Substrings of key names whose string values are safe to print.
SAFE_STRING_KEYS = ("plan", "tier", "period", "unit", "type_name", "state")

# Substrings that mark a field as quota-relevant, for the summary section.
QUOTA_HINTS = ("credit", "quota", "usage", "used", "included", "limit",
               "remaining", "capabilit", "bandwidth", "minutes", "invocation")


def redact(key, value):
    """Numbers and booleans pass through; strings are withheld by default."""
    if isinstance(value, bool) or isinstance(value, (int, float)):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        k = key.lower()
        if any(s in k for s in SAFE_STRING_KEYS) and len(value) <= 40:
            return value
        return f"<str len={len(value)}>"
    return f"<{type(value).__name__}>"


def walk(node, path=""):
    """Yield (dotted_path, key, scalar_value) for every leaf."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")
    else:
        key = path.split(".")[-1].split("[")[0]
        yield path, key, node


def main():
    token = os.environ.get("NETLIFY_AUTH_TOKEN", "").strip()
    if not token:
        print("FAIL: NETLIFY_AUTH_TOKEN is empty or unset.")
        print("Check the secret name at Settings > Secrets and variables > Actions.")
        return 1

    req = urllib.request.Request(
        API,
        headers={"Authorization": f"Bearer {token}",
                 "User-Agent": "netlify-quota-probe"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"FAIL: HTTP {e.code} from {API}")
        if e.code == 401:
            print("401 means the token is invalid, expired, or revoked.")
        elif e.code == 403:
            print("403 means the token is valid but lacks access to accounts.")
        return 1
    except urllib.error.URLError as e:
        print(f"FAIL: could not reach {API}: {e.reason}")
        return 1

    print(f"HTTP {status} from {API}")

    try:
        accounts = json.loads(body)
    except json.JSONDecodeError:
        print("FAIL: response was not JSON. Body withheld (may contain account data).")
        return 1

    if not isinstance(accounts, list):
        accounts = [accounts]
    print(f"accounts returned: {len(accounts)}")
    if not accounts:
        print("No accounts on this token. Nothing to report.")
        return 1

    for i, acct in enumerate(accounts):
        print(f"\n===== account[{i}] — full field inventory (strings redacted) =====")
        leaves = list(walk(acct))
        for path, key, value in leaves:
            print(f"  {path} = {redact(key, value)!r}")

        print(f"\n----- account[{i}] — quota-relevant numeric fields -----")
        hits = [
            (p, v) for p, k, v in leaves
            if any(h in p.lower() for h in QUOTA_HINTS)
            and isinstance(v, (int, float)) and not isinstance(v, bool)
        ]
        if hits:
            for p, v in hits:
                print(f"  {p} = {v}")
        else:
            print("  none — no numeric field matched a quota keyword.")
            print("  Read the inventory above to find what this plan actually exposes.")

    print("\nDone. Raw response deliberately not printed (public repo, public logs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
