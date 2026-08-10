# BaseBloom Data — the 90-day execution plan

**Window: Mon 10 Aug 2026 → Sat 7 Nov 2026 (13 weeks).**
Strategy, feasibility analysis and vendor verification live in
[`basebloom-bi-strategy.md`](./basebloom-bi-strategy.md). This document is the
execution detail only: what gets done, in what order, by when, and how you know
it is done.

---

## Operating parameters

| | |
|---|---|
| Capacity | 10–15 hrs/week, evenings and weekends, around a full-time role |
| Total budget of hours | ~130–195 hrs across 13 weeks |
| Platform spend, weeks 1–13 | **~$14/mo** (one Power BI Pro license). No Fabric capacity is bought inside this window unless Gate C fires. |
| One-time spend | Georgia LLC filing (~$100), domain/analytics (~$0–$10/mo), optional E&O quote |
| Entity | BaseBloom LLC (Georgia) — filing is a Week 4 deliverable |
| Employment conflict | Confirmed none. Day-job hygiene rules in strategy §4 still apply. |
| Platform decision | Power BI / Fabric. Tableau is a competency, not the product. See strategy §2.4. |

### Hour budget by phase

| Phase | Weeks | Est. hours | Theme |
|---|---|---|---|
| 1 — Foundation | 1–4 | ~50 | Make the existing promise true |
| 2 — Product & pipeline | 5–8 | ~50 | Publish the offer, fill the funnel |
| 3 — Deliver & decide | 9–13 | ~55 | Ship one engagement, systematize, review |

### Targets — set these now, review them at Gate D

| Metric | Target by Day 90 | Why this number |
|---|---|---|
| Care-plan clients receiving an automated report | 100% | It is already contractually owed |
| Qualified Tier 2 conversations | 8 | ~4 needed to close 1 at a realistic SMB rate |
| Tier 2 engagements signed | 1 | Proves the offer, not the market |
| Tier 2 revenue booked | $2,000–$5,000 | One build at list |
| New MRR added | $150–$400 | One data care plan |
| Realized hourly on engagement #1 | ≥ $100/hr | Below this, the price is wrong, not the client |
| Manual hours spent on monthly reporting | ≤ 30 min/client/mo | The whole point of Week 2 |

> **Deliberately not a target: revenue.** Ninety days with a 10-hr week buys you
> one delivered engagement and a repeatable system. Anyone promising more is
> selling you something.

### Decision gates

| Gate | When | Question | If it fails |
|---|---|---|---|
| **A** | End W2 | Does the report generator produce a correct report for a real client with no manual editing? | Stop feature work. Fix the pipeline. Everything downstream depends on it. |
| **B** | End W5 | Is the Data offer live on the site without regressing LCP/CLS? | Ship the offer as a plain page; do not let design polish block sales. |
| **C** | End W8 | Is there a signed Tier 2 engagement, or ≥3 qualified conversations? | Do not build. Re-run discovery on a different segment before spending W9–10. |
| **D** | End W13 | Realized hourly ≥ $100 and ≥1 client renewing? | Choose explicitly: reprice, narrow the ICP, or shut the line down. |

---

# Phase 1 — Foundation (Weeks 1–4)

**Phase goal:** BaseBloom can honestly deliver the report it already sells, has
one public proof asset, and is a real legal entity.
**Nothing new is sold in this phase.**

---

## Week 1 · Mon 10 Aug – Sun 16 Aug — Instrument and inventory

**Objective:** know exactly what data exists, for whom, and start collecting it.
Today you cannot deliver the report the site promises three times over
(`index.html:452`, `:455`, `:487`) because the live build makes zero
third-party requests.

### Tasks

1. **Pick and install analytics.** Requirement: cookieless (no consent banner),
   <2 KB, no third-party render-blocking, self-hostable or single-endpoint.
   Candidates: Plausible, Fathom, Umami (self-host). Install on
   `basebloomdesign.com` first.
   - Load it `defer`, after the fold. The site's measured mobile LCP is 428 ms —
     that number is a sales asset, do not spend it on a tag.
2. **Roll analytics to every care-plan client site.** One deploy each. Record
   the site → property mapping in a tracking sheet.
3. **Connect Google Business Profile.** Get API access to each client's GBP
   (Business Profile Performance API). Confirm you have owner or manager rights
   on every listing — chase the ones you don't; you cannot report on a listing
   you cannot read.
4. **Add call tracking.** The hero `tel:` link (`index.html:330`) is the
   highest-intent action on every BaseBloom site and currently generates no
   data. Minimum: a click event on every `tel:` link. Better: a tracking number
   that forwards, if the client accepts it.
5. **Build the client data inventory.** One row per care-plan client, one column
   per source, marked *available / needs access / doesn't exist*.
6. **Lock the metric set.** Ship exactly these seven; refuse the rest:

   | Metric | Source | Definition |
   |---|---|---|
   | Calls | `tel:` click events | Distinct sessions with ≥1 tel click |
   | Form submissions | Netlify Forms | `demo-request`-equivalent per client |
   | Site visits | Analytics | Unique visitors, 28-day window |
   | GBP views | GBP API | Profile impressions, search + maps |
   | GBP actions | GBP API | Calls + direction requests + website clicks |
   | Search terms | GBP API | Top 10 queries surfacing the listing |
   | Reviews | GBP API | New reviews and rating delta in period |

   No bounce rate, no time-on-page, no "engagement". A trades owner cannot act
   on them and they invite arguments you cannot win.
7. **Verify Fabric F2 pricing** in the Azure pricing calculator for `East US 2`
   (or your region). This is the last unverified number in the strategy — the
   licensing question is settled (strategy §2.2), the price is not.

### Deliverable
Analytics live on all properties; `client-data-inventory.md`; a one-page metric
definition sheet.

### Definition of done
You can name, for every care-plan client, which of the seven metrics you can
actually produce — and you have a written reason for every gap.

**Est. 12 hrs.** *Risk: GBP access chases are slow and depend on clients
responding. Start those on day 1; do everything else while waiting.*

---

## Week 2 · Mon 17 Aug – Sun 23 Aug — Build the report generator once

**Objective:** the highest-leverage build in the plan. Written once, amortized
across every current and future care-plan client, and it converts a recurring
manual chore into a product.

**Stack:** Evidence.dev → static build → Netlify. Rationale in strategy §2.1:
no iframe, full design control, responsive, ~$0 runtime, and it deploys onto
infrastructure already in use.

### Tasks

1. **Scaffold the Evidence project.** One repo, `basebloom-reports`.
2. **Write the ingest job.** Scheduled (nightly is plenty — see strategy §2.5):
   GBP API + analytics API → normalized tables → DuckDB/Parquet committed or
   cached for the build.
   - Idempotent: re-running for the same period must not double-count.
   - Retry with backoff on API failure, and **fail loudly**. A silently stale
     report is worse than no report.
3. **Build the report template.** One template, parameterized by client. Sections
   in this order — it mirrors how the owner thinks, not how the data is shaped:
   1. *The number that matters* — calls this month vs last, one big figure
   2. *Where the calls came from* — GBP vs site vs direct
   3. *What people searched* — top 10 terms
   4. *Your reviews* — new reviews, rating, unanswered count
   5. *What we did this month* — hand-written, 3 bullets max
   6. *What we're doing next month* — hand-written, 3 bullets max
4. **Apply the BaseBloom design system.** Ink `#101C13`, bloom green `#16B364`,
   sand `#D8C6A0`, brown `#C89253`. Prata for display, Inter for body — and per
   the hero audit, **do not use Prata below ~16px**; it ships one weight and
   degrades at small sizes. Charts follow the same palette; green means the
   client's number, never "good".
5. **Handle the missing-data case explicitly.** If a source is unavailable, the
   report says so in plain language. It never renders a zero as if it were a
   measurement. This is the single most important correctness rule in the build.
6. **Generate for one real client and reconcile by hand** against the GBP and
   analytics consoles, metric by metric.
7. **Test at 390 px.** Most owners will open this on a phone.

### Deliverable
`basebloom-reports` producing a correct, branded, mobile-clean report for at
least one real client from a single command.

### Definition of done
Every one of the seven metrics reconciles by hand against source consoles.
Sections 5 and 6 are the *only* manual input, and take under 10 minutes.

> ### 🚦 Gate A — end of Week 2
> **Correct report, no manual editing?** If no, stop and fix. Do not proceed to
> Week 3. Everything after this depends on the pipeline being trustworthy, and a
> reporting product that is wrong once is dead.

**Est. 15 hrs.** *This is the week to protect. If something has to slip, slip
Week 3, not this.*

---

## Week 3 · Mon 24 Aug – Sun 30 Aug — The showcase dashboard

**Objective:** one public artifact that proves BI capability and fixes the site's
weakest scored dimension. The hero audit puts Distinctiveness at **7.0/10**,
lowest of eight, because the site *"shows the customer's job, not BaseBloom's
craft"* — trades b-roll any agency could run.

### Tasks

1. **Choose the subject: BaseBloom's own business.** Real leads, real demos
   built, real days-to-launch, real care-plan retention.
   - **Non-negotiable: no synthetic numbers.** The site's own source comment
     sets the standard — *"every claim here is verifiable. No invented reviews or
     clients."* A fabricated dashboard is disqualifying in a category whose
     entire product is numerical honesty. If BaseBloom's own numbers are thin,
     say so on the page; small and true beats large and invented.
2. **Build it in Power BI Desktop.** Six to eight visuals maximum. Theme JSON
   matching the BaseBloom palette. **Author a phone layout** — embedded Power BI
   is non-responsive by default and this is where it looks worst.
3. **Publish to web.** Free, no capacity required. Legitimate here precisely
   because the data is BaseBloom's own and public-safe. **Never for a client** —
   there is no authentication and RLS is unsupported (strategy §2.3).
4. **Build the `/data` route.** Dashboard below the fold, lazy-loaded via
   `IntersectionObserver`, inside an `aspect-ratio` container so the iframe
   reflows. Above the fold: a static hero explaining the offer, so the page is
   useful before the iframe resolves.
5. **Measure.** Throttled 4G, 4× CPU. If the embed is unacceptable on mobile,
   ship a static Evidence version of the same dashboard as the primary and
   demote the live embed to a "see it live" link. **Design quality wins over
   platform loyalty.**

### Deliverable
`/data` live with a real, working dashboard.

### Definition of done
Loads acceptably on a throttled phone. The hero of `/` is untouched and its LCP
is unchanged.

**Est. 12 hrs.**

---

## Week 4 · Mon 31 Aug – Sun 6 Sep — Entity, paperwork, first reports out

**Objective:** be a real company before money and client data move; put the first
automated reports in clients' hands.

### Tasks

1. **File BaseBloom LLC (Georgia).** In order: Articles of Organization with the
   Georgia Secretary of State → EIN from the IRS → business bank account →
   invoicing moved onto the entity.
   - **Time-sensitive.** The footer already reads *"BaseBloom LLC · Atlanta,
     Georgia"* (`index.html`), so until the filing is effective the site is
     claiming a legal status that does not exist. Either the filing lands or the
     footer changes; leaving both as-is is not an option.
2. **Paper the data relationship.** A confidentiality / data-processing addendum
   to the existing agreement covering: what data you access, where it is stored,
   how long you keep it, what happens on termination, and breach notification.
   Mirror the tone of the existing FAQ — *"nothing is held hostage"* — because
   ownership clarity is already the strongest trust copy on the site.
3. **Get an E&O quote.** Tech E&O with a cyber endorsement. You do not have to
   buy it in Week 4; you do have to know the number before quoting Tier 2.
4. **Send the first automated reports** to every care-plan client.
5. **Attach one question to each report:** *"Would it be useful to see your
   jobs, quotes and revenue in something like this?"* This is Tier 2 discovery
   disguised as service, and it costs nothing.

### Deliverable
LLC filed; DPA addendum signed by care-plan clients; first reports delivered;
responses logged.

### Definition of done
Every care-plan client has received an automated report, and each response is
recorded as *interested / not now / no data*.

**Est. 11 hrs.**

---

# Phase 2 — Product and pipeline (Weeks 5–8)

**Phase goal:** the offer is public, priced, papered, and has real conversations
behind it.

---

## Week 5 · Mon 7 Sep – Sun 13 Sep — Ship the site changes

**Objective:** publish the Data service line, and fix the hero defects while you
are already in the codebase.

### Tasks — Data service line

1. **Add a Data section**, modeled on `#pricing`/`#how`. Reuse `.price`,
   `.step`, `.section-head`, `.reveal` so it inherits the reveal/spot animation
   registered at `index.html:564`.
2. **Give Data its own pricing block.** Do *not* add a fourth card to
   `.pricing` — `index.html:226` is `repeat(3,1fr)` with breakpoints at 900px
   (2-up) and 640px (1-up), and a 4-up desktop row crowds both ladders. Two
   separate three-card blocks read better and keep the web offer intact.
3. **Nav** (`index.html:309-316`): add `Data` before `Pricing`.
4. **Two FAQ entries** in the `458-489` pattern, matching the existing
   ownership-first voice:
   - *"Do I need a Power BI license?"* → **"No. You just open a web page.
     Licensing sits with us."** (Verified: app-owns-data end users are
     unlicensed — strategy §2.2.)
   - *"Who owns the dashboard?"* → same answer as the website: you do.
5. **Write the Data section copy.** Lead with the outcome, not the tooling. The
   headline is not "Power BI dashboards"; it is closer to *"Know which jobs
   actually make money."*

### Tasks — hero audit Wave 1 (~1–2 days, six of eight dimensions to 9)

6. **Fix the mobile `h1` first.** `.hero h1{clamp(2.6rem,5.5vw,4.1rem)}` is never
   overridden below 720px, so at 390px it floors at 41.6px in a 342px column —
   a four-line wrap that strands "base." and destroys the two-line white/green
   split. This is the worst visible defect on the site.
7. **Add `:focus-visible` rings.** Currently zero occurrences; the one real
   accessibility gap.
8. **Deduplicate the fonts — ~128 KB of pure waste, fixable in CSS.** The site
   declares nine `@font-face` rules against nine URLs, but `public/basebloom/fonts/`
   contains only **four distinct files**:

   | Family | URLs declared | Distinct files | Reality |
   |---|---|---|---|
   | Inter | 3 (400/500/600) | 1 | Variable font, `wght` axis 100–900 |
   | JetBrains Mono | 2 (400/500) | 1 | Variable font, `wght` axis 400–800 |
   | Space Grotesk | 3 (500/600/700) | 1 | Declared but never used |
   | Prata | 1 | 1 | Static, correct as-is |

   Each URL is a separate cache entry, so a browser using Inter 400, 500 and 600
   downloads the *same 48,256-byte file three times*. Same for JetBrains Mono at
   two weights — which is the ~60 KB the hero audit noticed but attributed to the
   font being heavy rather than duplicated.

   Fix: collapse each family to one rule with a weight range, e.g.
   `@font-face{font-family:'Inter';font-weight:100 900;src:url('fonts/inter-400.woff2') format('woff2')}`.
   **Saves ~96 KB (Inter) + ~31 KB (JetBrains Mono) ≈ 128 KB** with no visual
   change. Drop the three Space Grotesk declarations entirely.
9. **Fix the `og:image` path** — it points at `hero-poster.jpg`; the actual file
   is `trades-hero-poster.jpg`, and the URL is relative, which most scrapers
   won't resolve. Every share of this site is currently rendering without an
   image.

### Definition of done
Data section live. Contrast sampler (`docs/basebloom-hero-audit/contrast-sampler.mjs`)
passes AA. LCP/CLS at or better than baseline: desktop 1080 ms / CLS 0,
mobile 428 ms / CLS 0.0531.

> ### 🚦 Gate B — end of Week 5
> **Offer live without perf regression?** If the design isn't finished, ship a
> plain, correct Data page anyway. Sales conversations in Week 8 need a URL, not
> a masterpiece.

**Est. 14 hrs.**

---

## Week 6 · Mon 14 Sep – Sun 20 Sep — The flagship case study

**Objective:** convert the single strongest asset you already own — dozens of
delivered dashboards with measurable impact, plus employee enablement — into
sales collateral.

### Tasks

1. **Ask for consent in writing.** Offer three levels and let them pick: named
   with logo / industry-only anonymous / anonymous with obfuscated figures.
   Anonymous is still worth publishing.
2. **Interview the client for 30 minutes.** Five questions, and the specificity
   here is what makes the case study work:
   - What was the reporting process before?
   - How long did it take, and who did it?
   - What decision did you make from the dashboard that you couldn't before?
   - What broke, and how did we handle it?
   - What would you tell someone considering this?
3. **Write it in the site's voice** — plain, specific, no superlatives. Structure:
   situation → what was actually built → what changed, with numbers → what it
   costs to keep running.
4. **Quantify honestly.** "Cut monthly reporting from ~6 hours to ~20 minutes" is
   credible and checkable. "Increased revenue 40%" is not, and you cannot prove
   causation.
5. **Build a redacted screenshot set.** Real layout, obfuscated figures. Label
   them as obfuscated.
6. **Formalize that client onto a retainer** under BaseBloom LLC if they aren't
   already. Existing revenue on paper is worth more than new revenue in
   conversation.
7. **Publish to `/data/case-study`** and link it from the Data section.

### Deliverable
One published case study; one formalized retainer.

### Definition of done
Written consent on file. Every number in it traceable to something you can show.

**Est. 10 hrs.**

---

## Week 7 · Mon 21 Sep – Sun 27 Sep — Price it and paper it

**Objective:** you cannot sell in Week 8 without a price, a scope and a contract.
Improvising these under sales pressure is how solo consultants underprice.

### Tasks

1. **Publish the Data ladder.** Mirror the web ladder's shape — one-time build
   plus monthly care — because that shape already converts for this business.

   | SKU | Price | Scope |
   |---|---|---|
   | Data health check | **$500**, credited toward a build | Source audit, feasibility, a written findings memo |
   | Dashboard build | **$2,000–$5,000** | 1 source, up to 8 visuals, one refresh schedule, 2 revision rounds |
   | Extra source | **+$750–$1,500** each | Per additional system |
   | Data care plan | **$300–$800/mo** | Hosting, refresh monitoring, alerting, monthly review call, small changes |
   | Bundled care add-on | **+$150–$400/mo** | Same, attached to an existing site retainer |
   | Automation build | **~$1,200–$1,600/day** | Refresh chains, Power Automate, alerting |
   | Team enablement | **$1,500–$3,000/cohort** | Half-day training, recorded, with a workbook |

   Rate basis: senior US independents transact at **$150–$225/hr**. Ignore the
   $56–$87 marketplace averages — that is an offshore commodity market you are
   not in.

2. **Mirror the existing terms exactly:** 50% up front, two revision rounds,
   month-to-month care, client owns everything. Reusing proven terms removes
   friction you'd otherwise have to re-earn.
3. **Write the data-readiness checklist.** This is the money document — it stops
   you fixed-pricing a build on data that doesn't exist.

   | Check | Disqualifying answer |
   |---|---|
   | What system holds jobs/appointments/orders? | "A spreadsheet Karen maintains" |
   | Can we get an API key or scheduled export? | "No, and the vendor charges for API access" |
   | How many rows/month? | Under ~100 — a report, not a dashboard |
   | Who will read this, by name? | "Not sure" — no owner means no renewal |
   | What decision changes because of it? | No answer — this is a vanity project |
   | Is historical data clean and consistent? | Schema changed mid-year, no backfill |

   **Two or more disqualifying answers → quote a paid Data health check only,
   never a fixed-price build.**
4. **Write the SOW template.** Must contain: named data sources, refresh
   frequency, visual count, revision rounds, what is explicitly out of scope,
   change-order rate, and who supplies credentials.
5. **Write the "no" script.** Rehearse it: *"Your data isn't ready for a
   dashboard yet, and building one now would cost you money and tell you
   nothing. Here's what would need to be true first."* Refusing badly-fitting
   work is the same instinct as *"No ranking promises"* — the line the hero audit
   credits as the site's strongest differentiator.
6. **Build the 12-slide pitch deck**, reusing the case study.

### Deliverable
Published pricing, SOW template, readiness checklist, pitch deck.

### Definition of done
You can quote a real prospect end-to-end without writing anything new.

**Est. 12 hrs.**

---

## Week 8 · Mon 28 Sep – Sun 4 Oct — Sell

**Objective:** fill the funnel. This is a sales week, not a build week — resist
the urge to code.

### Tasks

1. **Offer a free dashboard audit to every care-plan client.** Reuse the proven
   mechanic: the site's free-demo step (`index.html:436`) is exactly this move,
   already validated for this buyer. *"We build a real demo, free"* becomes
   *"We'll map your data, free."*
2. **Work the Week 4 responses.** Anyone who answered *interested* to the report
   question is a warm inbound.
3. **Call five existing clients and ask directly what they'd pay.** No public
   data on SMB willingness-to-pay for embedded dashboards is defensible — I
   looked. Five calls beat any further research.
4. **Target 20 outbound conversations** in fitting verticals — dental and medical
   practices, restaurants, gyms and studios, home services on Jobber /
   ServiceTitan / Housecall Pro, property management, insurance agencies. All
   have a real transactional system, which is the qualifier that matters.
5. **Run every prospect through the readiness checklist before quoting.** No
   exceptions, including for people you like.
6. **Publish one piece of proof content** — a short teardown of the showcase
   dashboard: what it measures, why those metrics, what it cost to build.

### Deliverable
A pipeline sheet: name, vertical, source system, readiness score, stage, next step.

### Definition of done
≥8 qualified conversations held. ≥1 signed engagement or ≥3 at proposal stage.

> ### 🚦 Gate C — end of Week 8
> **Signed engagement, or ≥3 qualified conversations?** If neither, **do not
> build anything in Weeks 9–10.** Spend them re-running discovery on a different
> segment. Building unsold product is the most expensive possible use of the
> remaining hours.

**Est. 12 hrs — mostly calls, not code.**

---

# Phase 3 — Deliver and decide (Weeks 9–13)

---

## Weeks 9–10 · Mon 5 Oct – Sun 18 Oct — Deliver engagement #1

**Objective:** ship one real Tier 2 engagement, and learn whether the price is right.

### Tasks

1. **Track every hour against the quote, in 15-minute blocks.** The engagement's
   real product is this number. Everything else you already know how to do.
2. **Week 9 — discovery and pipeline.** Credentials, source connection, model
   the data. Expect this to consume 50–60% of total effort; source connectivity
   is where SMB BI work bleeds margin, not visual design.
3. **Week 9 — set the refresh cadence.** Default to nightly Import. Do not build
   real-time because it's impressive; strategy §2.5 covers why.
4. **Week 10 — build, review, hand over.** Two revision rounds as scoped, then
   change orders. Hold the line — scope creep on engagement #1 sets the
   precedent for every engagement after.
5. **Decide the hosting path per §2.2's progression.** Client tenant if they have
   Microsoft 365 (their licensing, their bill, your fee); static Evidence build
   if the data is small and refresh is nightly; **only** stand up F2 if neither
   fits.
6. **Deliver an enablement session** as part of handover. It reduces support
   load, and it seeds the training SKU.
7. **Attach the care plan at signature.** Never deliver a dashboard without one —
   an unmaintained dashboard is a liability that will eventually be blamed on you.

### Deliverable
Live dashboard, documented refresh, signed care plan, and an honest hours log.

### Definition of done
Client has opened it unprompted at least twice. Refresh has run unattended for
seven consecutive days.

**Est. 25 hrs across both weeks.**

---

## Week 11 · Mon 19 Oct – Sun 25 Oct — Systematize

**Objective:** make engagement #2 take 60% of the hours of engagement #1.

### Tasks

1. **Extract a semantic-model starter** — standard date table, naming
   conventions, a base measure library (period-over-period, running totals,
   rolling averages).
2. **Publish the theme kit** — Power BI theme JSON in the BaseBloom palette, plus
   matching Evidence components, so both paths look like one studio.
3. **Write the refresh-monitoring runbook.** What alerts, who gets paged, what
   the first three diagnostic steps are. **This is what the care plan actually
   sells** — dashboards break loudly when a source schema changes, and that
   fragility is the honest justification for a recurring fee.
4. **Write the client onboarding checklist** — credentials, access, a named
   contact, the review-call cadence.
5. **Package team enablement as a SKU.** You have done this successfully before.
   It is the highest-margin, lowest-delivery-risk item in the ladder and the only
   one that doesn't scale with your hours.
6. **Write the post-mortem on engagement #1**: quoted vs actual hours, what took
   longest, what you'd scope differently, what to add to the readiness checklist.

### Deliverable
A reusable delivery kit and a written post-mortem.

**Est. 12 hrs.**

---

## Week 12 · Mon 26 Oct – Sun 1 Nov — Second pass at the funnel

**Objective:** prove repeatability with a warm second sale, using real proof
instead of promises.

### Tasks

1. **Re-approach every Week 8 conversation** that didn't close — now with a
   delivered engagement, a case study, and a live dashboard.
2. **Ask engagement #1 for a referral and a testimonial.** Best moment is right
   after a successful handover.
3. **Quote using the post-mortem's real hours**, not Week 7's estimates.
4. **Run the F2 decision.** Buy capacity only if ≥3 clients need hosted embedding
   *or* one client's data genuinely can't be served statically. Two-week PAYG
   trial with a representative model before any reservation — F2 is *licensed*
   for app-owns-data but at 2 CU / 0.25 v-cores its performance is unproven
   (strategy §6, item 2).
5. **Review the platform bill** against Data revenue. Idle capacity is the one
   thing that can quietly make this unprofitable.

**Est. 10 hrs.**

---

## Week 13 · Mon 2 Nov – Sat 7 Nov — Review and decide

**Objective:** an honest verdict against numbers committed in Week 0.

### Tasks

1. **Fill in the scorecard.**

   | Metric | Target | Actual |
   |---|---|---|
   | Care-plan clients on automated reports | 100% | |
   | Qualified Tier 2 conversations | 8 | |
   | Engagements signed | 1 | |
   | Revenue booked | $2,000–$5,000 | |
   | New MRR | $150–$400 | |
   | Realized hourly, engagement #1 | ≥$100 | |
   | Manual reporting time per client | ≤30 min/mo | |
   | Platform spend | ~$14/mo | |

2. **Answer four questions in writing:**
   - Did Tier 1 reduce churn or increase care-plan conversations?
   - Was the Tier 2 price right? (Realized hourly is the whole answer.)
   - Which vertical converted best, and is it worth specializing?
   - Was BI a *distraction* from web revenue, or a multiplier?
3. **Make the call, explicitly. One of three:**
   - **Expand** — Data becomes a co-equal line; build a dedicated landing page,
     set a Q1 target, consider F2 reserved.
   - **Attach-on** — Data stays an upsell to web clients only. No separate
     marketing. Lowest risk, and a legitimate answer.
   - **Stop** — Keep Tier 1 reporting (it's owed anyway), retire Tier 2. Write
     down why, so you don't relitigate it in six months.
4. **Write the next 90 days** based on the answer.

**Est. 6 hrs.**

---

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Care-plan clients have no data worth reporting | **High** | Medium | Tier 1 is deliberately GBP + analytics only; it works with the thinnest possible data |
| No Tier 2 demand in the trades base | **High** | High | Gate C forces a segment pivot at W8 instead of W13; outbound targets non-trades verticals from the start |
| Fixed-price build on unqualified data | Medium | **High** | Readiness checklist (W7) is mandatory; ≥2 disqualifiers → health check only |
| F2 too small for real embedded load | Medium | Medium | No capacity purchased until W12, and only after a PAYG trial |
| Embedded Power BI is too slow on mobile | Medium | Medium | Static Evidence path is the default; embedding is the exception |
| Time crunch from the day job | **High** | Medium | Gates let you stop cleanly at W2, W5 or W8 with something finished |
| A dashboard breaks and gets blamed on you | Medium | **High** | Never ship without a care plan; monitoring runbook in W11 |
| Brand dilution from generic BI | Medium | Medium | Trades stays the front door; Data is a separate section, not a rewritten hero |
| LLC filing lags the footer claim | Medium | Medium | W4 task 1; if it slips, change the footer instead |

## What this plan deliberately does not do

- **No Fabric capacity purchase inside 90 days** unless a paying client forces it.
- **No Tableau build.** It is a competency, not the product (strategy §2.4).
- **No real-time pipelines.** Sold as a differentiator, not built by default.
- **No second service brand.** One brand, two lines, one funnel.
- **No revenue target beyond one engagement.** At 10–15 hrs/week, one delivered
  engagement plus a repeatable system is the honest ceiling.
