# Project notes

## Metered MCP balance reporting

**Standing instruction.** In any response whose turn used a metered MCP
server, report at the end of the response, after the substantive answer:

- **Used / total** for the plan, as a numerator over a denominator
- **Remaining**, as a separate figure

Report the real numbers only. Do **not** invent, estimate, or infer them. If a
figure is unreachable, say so and name the reason rather than omitting it.
Where a reader returns a remaining balance with no plan total, report the
remaining figure and say there is no denominator — do not manufacture one.

`.claude/hooks/mcp-balance-reminder.py` fires on `PostToolUse` for these
servers and injects the reminder, once per server per turn. It cannot fetch
the figures itself: these are claude.ai connectors authenticated server-side,
and no token for them reaches this container, so no shell script can query
them. Adding a server means adding it to the script's `METERED` map *and* to
the `PostToolUse` matcher in `.claude/settings.json`.

| Server | Reader tool | Verified 2026-08-10 |
|---|---|---|
| Higgsfield | `mcp__Higgsfield__balance` | works — `credits`, `subscription_plan_type`; remaining only, no plan total |
| Cloudinary | `mcp__Cloudinary__get-usage-details` | works — `credits.usage` / `credits.limit` / `credits.used_percent` |
| Lovable | `mcp__Lovable__get_workspace` | documents a credit balance but returned none for the free workspace |
| Netlify | none | blocked, see below |

Do not use `mcp__Higgsfield__show_plans_and_credits` as a reader — it opens a
purchase widget rather than quietly returning a figure.

### Netlify specifically

**This cannot be satisfied yet.** Checked 2026-08-09:

- The Netlify MCP server exposes only `get-user`, `get-teams`, `get-team`,
  plus project/deploy/extension readers. The team object returns
  `created_at`, `enforce_mfa`, `members_count`, `slug`, `updated_at`, `id`,
  `name`, `type_name` and a role/URL enrichment — **no billing, quota, usage
  or credit fields of any kind**.
- No `NETLIFY_AUTH_TOKEN` in the environment and no Netlify CLI installed, so
  the REST API is not reachable either.

Do **not** invent, estimate, or infer these numbers. If a response touches
Netlify credits while this is still true, say the figures are unavailable and
name the reason, rather than omitting the topic silently.

**To unblock**, one of:

1. Add a Netlify personal access token to the environment as
   `NETLIFY_AUTH_TOKEN`, then read
   `GET https://api.netlify.com/api/v1/accounts` — the account object carries
   `capabilities` with included/used figures.
2. Install the Netlify CLI and use an authenticated `netlify api` call.
3. Confirm which metric "credits" refers to. Netlify meters several things
   (bandwidth, build minutes, function invocations) and separately sells
   "credits" for agent/AI features; the right endpoint depends on which.

## basebloom

`public/basebloom/` is a **byte-for-byte mirror of the live
basebloomdesign.com build**, fetched 2026-08-09. It is not generated from
anything in this repo. Two consequences:

- Do not hand-edit it expecting the change to survive; a re-sync overwrites it.
- `basebloom-drift/` is the older Vite concept the live site has moved past.
  Its `outDir` was repointed from `../public/basebloom` to a local `dist/`
  precisely so a build cannot clobber the mirror.

Edits applied on top of the mirror — a re-sync must re-apply these:

1. **Demo links.** Relative links to the nine demo sub-sites
   (`./slate-and-storm/` etc.) and to `/work` are absolutised to
   `https://basebloomdesign.com/...`, because the page is served under
   `/basebloom/` here and those directories are deliberately not mirrored.

2. **The full hero loop.** The live site ships `trades-hero-loop.mp4`, a
   6.13 s exterior-only montage. That is the *second half* of a two-part
   sequence — the first half, a pull-back from an electrician steadying a
   glowing Edison pendant bulb out through the bay window, was generated but
   never deployed. Both files are still in `public/basebloom/`; the page now
   points at the reassembled version:

   - `trades-hero-loop-full.mp4` — 10.54 s, 1920×1080, 2624 kb/s, 3 379 KB.
     Higgsfield take `378656c3` (the one clean of the door artifact that
     spoils takes `8841252d` and `c7f7b1ec`) joined to the live montage from
     its frame 6, where the two align. 0.4 s crossfade hides a bay-window
     content swap at the join; 0.35 s fade from black at the head so the
     loop closes black-to-black (first and last frame both luma 0).
   - `trades-hero-poster-full.jpg` — pulled from 0.55 s so the poster matches
     the video's opening rather than jumping from the old exterior still.

   Open question: mobile never plays the video (deliberate `saveData` gate),
   so the poster is all a phone ever sees. The bulb close-up is consistent
   with the video; the old exterior crew shot arguably sells the multi-trade
   offer better on a phone. A mobile-specific poster is a one-line change if
   that trade is worth making.

An audit of the live hero, with routes to a 9 on eight dimensions, is in
`docs/basebloom-hero-audit.md`.
