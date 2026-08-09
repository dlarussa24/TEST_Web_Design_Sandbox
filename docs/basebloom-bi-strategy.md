# BaseBloom → Web + BI: feasibility, architecture, and a 90-day plan

**Status: site findings source-verified; market figures unverified.** Everything
asserted about basebloomdesign.com is measured against the mirrored live build in
`public/basebloom/` and cited by line. Everything asserted about vendor pricing
is secondary-source only — see the evidence-quality warning below before quoting
any dollar figure. Deliverable is a **strategy and spec only**; no application
code changes here, matching the convention in `basebloom-hero-audit.md`.

## Context

BaseBloom (basebloomdesign.com) sells one thing today: custom websites for local
trades in Atlanta. Three SKUs, live on the page now
(`public/basebloom/index.html:450-452`):

| SKU | Price | Recurrence |
|---|---|---|
| One-time build | $750–$1,500 | once |
| Local search setup | $500–$750 | once |
| Care plan | $100–$250/mo | monthly |

David LaRussa runs it as a sole proprietorship trading as "Built by David."
Separately he is a senior manager of business intelligence at a supply-chain
company, and his strongest skill is not web design — it is Power BI / Tableau
development and Microsoft-stack data engineering (Dataflows Gen2,
lakehouse/warehouse, Power Automate refresh chains, source-to-visual real-time
refresh). He has delivered dozens of dashboards to one primary external client,
plus employee enablement.

The asymmetry is the thing worth fixing: **BaseBloom monetizes his second-best
skill and ignores his best one.** A $1,500 website is a one-shot sale into a
price-sensitive market. A dashboard practice is a retainer sale into a market
where he is genuinely senior.

**Decisions already taken** (planning Q&A):
- One brand. BaseBloom is the studio with two service lines, Web and Data.
  "Built by David" is the legal entity that invoices.
- Buyers: existing BaseBloom web clients **and** SMBs of any vertical lacking a
  real BI/automation function. Not restricted to supply chain or ops.
- David carries a small fixed monthly platform cost, priced into the offer
  rather than passed through per client.
- No 90-day plan exists (`docs/` holds only the hero audit); this writes one.

### ⚠️ Evidence quality — read before quoting any number

Market research for this plan ran through a proxy that **blocked every external
vendor domain**. Zero primary sources were reachable — no Azure pricing
calculator, no learn.microsoft.com, no tableau.com. Every dollar figure below
comes from secondary search summaries, several from vendors who sell competing
products and have an incentive to distort incumbent pricing.

**Treat all figures as directional. Verify before any client proposal.** The
architecture does not depend on which exact tier wins; the pricing does.

---

## 1 · Feasibility verdict: yes — but as two products, not one

Adding dashboards is feasible and unusually well set up here, for reasons
specific to this business rather than generic encouragement.

**a. The promise is already sold.** This is the most important finding and it
reframes the project.

- `index.html:452` — the care plan promises *"a plain-English report showing
  what moved."*
- `index.html:455` — the no-ranking-promises clause resolves with *"We show you
  the numbers each month instead."*
- `index.html:487` — the FAQ commits to *"a one-page plain-English report
  showing what people searched and what moved."*

BaseBloom is already contractually a reporting business. The BI line does not
have to be invented and sold cold — it has to be productized out of work already
owed.

**b. The site cannot currently keep that promise.** Verified: the mirrored build
makes **zero third-party requests**. No GA4, no Plausible, no pixel, no tag
manager. The only external hosts referenced anywhere in `index.html` are
`basebloomdesign.com` and one Netlify demo subdomain. The monthly "numbers" can
therefore only be assembled by hand from Google Business Profile insights. That
is a live delivery risk today, and the cheapest, highest-credibility first build.

**c. The differentiator is real.** The hero audit's central finding
(`docs/basebloom-hero-audit.md:233`) is that the site *"shows the customer's job,
not BaseBloom's craft"* — trades b-roll any agency could run, scoring 7.0/10 on
distinctiveness, lowest of eight dimensions. A live dashboard of a client's own
numbers is the one asset a template shop cannot copy.

### The hard constraint

Local trades at $750–$1,500 are the wrong buyer for a *paid* dashboard. A
three-van plumber has no ERP and often no CRM; the only data that exists is GBP
insights, site analytics, call logs and maybe QuickBooks. That supports a
**reporting** product, not a **business intelligence** product, and it must be
near-zero marginal cost or it destroys care-plan margin.

So the offering splits in two. Conflating them is the main way this fails:

| | **Tier 1 — Reporting** | **Tier 2 — Analytics** |
|---|---|---|
| Buyer | existing BaseBloom trades clients | SMBs with no BI function, any vertical |
| Data | GBP, site analytics, calls, forms | real systems — POS, PMS, job software, ERP, finance |
| Delivery | automated, templated, built once, reused N times | bespoke engagement |
| Marginal cost | must be ~$0/client | priced in |
| Price | folded into the existing care plan | $2,000–$5,000 build + $300–$800/mo |
| Role | retention, proof, lead magnet | the actual revenue line |

Tier 1 is not a profit center. It makes Tier 2 sellable and it closes the gap in (b).

### The qualifying question that decides every deal

> **"What system are your jobs / appointments / orders in, and can I get an
> export or an API key?"**

If the answer is a spreadsheet someone maintains by hand, the engagement is a
data-cleanup project wearing a dashboard costume — price it as one or decline.
Good fits: dental and medical practices (practice-management systems),
restaurants and gyms (POS/booking), home services on Jobber / ServiceTitan /
Housecall Pro, e-commerce, property management, insurance agencies. Poor fits:
anyone whose only data is Google Analytics and a Square account — they need a
report, and Tier 1 already covers it.

Fixed-price dashboard builds on unqualified data sources are the classic way to
lose money on this work. Source connectivity, not compute, is what eats margin.

---

## 2 · How to tackle it — architecture

### 2.1 Do not put embedded Power BI on the trades sites

The instinct is to embed Power BI everywhere. Resist it for Tier 1, for four
reasons that all point the same way:

- **Cost shape.** Embedding for viewers without licenses ("app owns data")
  requires dedicated capacity — reportedly **Fabric F2 at ~$156/mo reserved or
  ~$262/mo PAYG**, plus one Power BI Pro license (~$14/mo) for authoring. That
  is a fixed platform cost spread across clients paying $100–$250/mo for
  *everything including hosting*.
- **Latency.** An embedded report is a heavyweight iframe: SDK bundle, token
  round trip, then render. Expect multiple seconds to first paint against a site
  whose measured mobile LCP is **428 ms** and desktop CLS is **0**.
- **Mobile.** Embedded Power BI is weakest exactly where trades customers live.
  The default iframe is fixed-dimension and non-responsive; a usable phone
  experience requires authoring a separate phone layout in Desktop, and page
  navigation isn't supported with mobile layout.
- **Brand.** An iframe you cannot style will never match Prata, the bloom green,
  or the sand palette. For a design-led studio that is the real objection.

For Tier 1 the right answer is a **statically generated report**: the pipeline is
real, the rendering is not live. A scheduled job pulls GBP + analytics, writes a
small dataset per client, and the page renders as BaseBloom's own HTML.

**Recommended tool: Evidence.dev.** It compiles SQL + Markdown into a static
site, version-controlled in Git, deployable to the Netlify setup already in use.
It is *your* HTML — no iframe, full design control, fully responsive, and
effectively zero runtime cost. Its one real limitation is that data is only as
fresh as the last build, which for "last month's numbers, correct, by the 3rd"
is not a limitation at all. A hand-built charting component over a small
Postgres/Supabase backend is an equally valid path if you'd rather own the code.

### 2.2 Reserve real embedding for Tier 2 — and buy capacity late

Embedding earns its cost when the client has real data, real users, and is
paying four or five figures. The economics are a **volume bet, not a per-client
cost**: F2 against one client at a $300/mo retainer is thin; F2 amortized across
ten clients is ~$16/client and excellent.

**So do not buy capacity in month one.** Recommended progression:

1. **Demo + clients 1–3** — Evidence.dev / hand-built, and *publish-to-web* for
   the showcase dashboard. $0 infrastructure. Prove the offering sells.
2. **Client 4+, or the first client with genuinely messy multi-source data** —
   stand up F2, ideally after a two-week PAYG trial with a representative model,
   then move to reserved once load is understood.
3. **Graduate clients to their own tenant** once they have Microsoft 365, which
   most SMBs above ~20 employees already do. Their licensing, their bill, your
   build fee and retainer. This is the scalable end state.

This means the platform cost baked into pricing is **~$14/month for the first
90 days**, not ~$170 — cheaper than the stated appetite, and the F2 decision
becomes trigger-based rather than a calendar item.

Design rules for when capacity does land:
- **Service principal, never a master user.** Registered Entra ID app, tenant
  setting scoped to a security group, server-side token generation only. Never
  ship the client secret to the browser.
- **Dynamic RLS from day one.** One semantic model, one report, a `TenantID`
  column, a DAX filter, `EffectiveIdentity` set at token-generation time. This is
  what makes one capacity serve N clients at near-zero marginal cost, and
  retrofitting it after client two is painful.
- **The tenant identity must come from your authenticated session — never from a
  URL parameter.** A `?tenant=42` passed into `EffectiveIdentity` is an IDOR that
  leaks every client's data to every other client. This is the single
  highest-consequence line of code in the system, and these clients will never
  audit you.
- **Pause dev capacity, never public-facing capacity.** PAYG F SKUs can be
  suspended (compute stops, storage continues); a business-hours schedule cuts
  roughly half. But a client dashboard has 11pm visitors and paused capacity has
  cold-start cost. Reserved capacity cannot be paused — reservation and pausing
  are mutually exclusive strategies.
- **Watch the refresh window, not the viewer count.** On a 2-CU F2 the practical
  risk is a heavy Dataflow Gen2 run burning the 24-hour background budget and
  throttling interactive queries — which on a client site means a *broken*
  dashboard, not a slow one. Prefer pipelines or notebooks over Dataflows Gen2
  for anything heavy, and schedule transforms off-peak.

### 2.3 Publish-to-web: use it for the demo, never for a client

Free, no capacity, no auth. Also: **no authentication whatsoever, and row-level
security is not supported.** Anyone who views source can lift the iframe URL.
New embed-code generation is reportedly off by default at the tenant level now.

That makes it perfect for exactly one thing — a **BaseBloom-owned showcase
dashboard built on BaseBloom's own real business data**, which costs nothing and
proves the capability. It is disqualified for anything client-owned. A
landscaping company's revenue by service line is not public data, and there is
no way to gate it.

### 2.4 Power BI vs Tableau vs everything else

**Lead with Power BI / Fabric.** It matches the deepest skill, most SMBs already
pay for Microsoft 365, and the Power Automate refresh-chain work is the
genuinely differentiated part of the offer.

**Do not build the embedded line on Tableau.** Reported floor is ~$5,000/year in
usage-based "analytical impressions" plus Creator seats — roughly 2–3× Power BI
at the small end, sales-gated, annually committed, with no published pricing. For
a solo operator that is friction with no upside. Keep Tableau as a competency for
clients already standardized on it. **Tableau Public is portfolio-only** — flat
files only, no database connections, no scheduled refresh, everything public.

**Ruled out for this segment:** Metabase (white-labeling, SSO, RLS and
interactive embedding all sit behind a ~$575/mo tier), Preset (~$500/mo for 50
viewer licenses, structurally wrong for anonymous viewers), self-hosted Superset
(a solo consultant maintaining Superset is a bad use of hours). **Looker Studio**
is the free fallback when capacity cost would kill a deal, accepting Google
branding and a non-reflowing iframe.

### 2.5 Refresh cadence — sell real-time, default to nightly

Almost no local business needs sub-10-second data. A dental office does not
decide anything on 2-second latency; the requirement is "correct by 8am."

- **Import mode, nightly or twice daily, handles ~90% of SMB work** — cheapest
  and most robust. Pro caps at 8 refreshes/day; capacity raises it to 48.
- **Incremental refresh** is the biggest CU saver on a growing fact table.
- **Direct Lake** is the default once data is already in a Fabric lakehouse —
  Import-class query speed with no refresh cost.
- **Real-time is a differentiator to sell, not a default to build.** Fabric
  Real-Time Intelligence is included in capacity with no separate SKU, which is a
  great pitch — but every real-time pipeline is a thing that breaks at 3am and
  you are one person. Price the on-call risk or don't offer it.
- **Build any real-time work on Fabric RTI (Eventstream → Eventhouse), not the
  classic streaming dataset API.** Push, streaming, and PubNub semantic models
  and streaming tiles are reportedly closed to new creation after **31 Oct 2027**.

### 2.6 What changes on the website

Scoped as spec, following the hero audit's convention — BaseBloom's site is a
separate codebase, so nothing in this repo is edited to ship it.

1. **A Data section**, modeled on the existing `#pricing` / `#how` markup and
   reusing `.price`, `.step`, `.section-head` and `.reveal` so it inherits the
   reveal/spot animation registered at `index.html:564`.
2. **Pricing grid.** `index.html:226` is
   `.pricing{grid-template-columns:repeat(3,1fr)}`, with breakpoints at 900px
   (2-up) and 640px (1-up). A fourth card needs the desktop rule to go 4-up;
   **preferred instead**: keep three web SKUs intact and give Data its own
   pricing block, so neither ladder gets crowded.
3. **Nav + FAQ.** Nav is `index.html:309-316`. The FAQ pattern at `458-489`
   should gain "Do I need Power BI licenses?" and "Who owns the dashboard?",
   mirroring the existing ownership answers — the strongest trust copy on the page.
4. **Analytics**, required before any reporting claim is honest. Pick something
   cookieless and lightweight so the zero-third-party profile and the absence of
   a cookie banner survive.
5. **The live demo dashboard page** — the proof asset and the distinctiveness fix.
   Real numbers only. The site's own source comment sets the standard: *"every
   claim here is verifiable. No invented reviews or clients."*

---

## 3 · The 90-day plan

Three 30-day phases. Effort assumes evenings and weekends around a full-time
senior manager role — roughly 10–15 hrs/week. That constraint is why the plan
front-loads reusable assets over bespoke client work.

### Days 1–30 — Make the existing promise true, and build the proof

Goal: BaseBloom can honestly deliver the report it already sells, and has one
public artifact proving dashboard capability. Nothing new is sold yet. Spend: ~$14/mo.

- **Week 1 — Instrument and verify.** Install analytics on basebloomdesign.com
  and every care-plan client site. Connect GBP. Inventory what data actually
  exists per client. Decide the metric set (calls, form fills, GBP
  views/searches/direction requests, review velocity) — no vanity metrics.
  **In parallel, resolve the F2 licensing question** (§6, item 1) — it is a
  ~$156/mo vs ~$8,400/mo question and everything downstream assumes the cheap answer.
- **Week 2 — Build the Tier 1 report generator once.** Scheduled pull →
  per-client dataset → templated Evidence.dev report. Highest-leverage build in
  the plan: written once, amortized across every current and future care-plan
  client, and it converts a manual monthly chore into a product.
- **Week 3 — The showcase dashboard.** Power BI on BaseBloom's own real business
  data, published via publish-to-web, embedded below the fold on a dedicated
  route. $0. Lazy-load it so it cannot touch hero LCP.
- **Week 4 — Legal and financial hygiene.** Three genuinely blocking items:
  1. **Resolve the entity discrepancy.** The footer reads *"BaseBloom LLC ·
     Atlanta, Georgia"* but the business is a sole proprietorship. Advertising an
     LLC that does not exist is real exposure, and it gets worse the moment
     contracts involve client production data. Form the LLC or correct the footer.
  2. **Check the employment agreement.** Selling BI consulting while employed as
     a senior BI manager can implicate non-compete, moonlighting, or
     IP-assignment clauses. Targeting non-supply-chain SMBs helps but does not
     settle it. Worth an attorney hour before the first BI invoice, not after.
  3. **Data handling.** Client production data is a different liability class
     than website photos. Need a confidentiality/DPA addendum; price E&O insurance.

### Days 31–60 — Productize and sell into the warm base

Goal: the offer exists publicly and the first paid Tier 2 engagement is signed.

- **Week 5 — Ship the site changes** from §2.6. Apply the hero audit's Wave 1
  CSS fixes in the same pass — ~1–2 days, takes six of eight dimensions to 9 —
  since you are in the codebase anyway. The mobile `h1` defect
  (`clamp(2.6rem,5.5vw,4.1rem)` never overridden below 720px, producing a
  four-line wrap at 390px) is the one to fix first.
- **Week 6 — Convert the existing BI client into the flagship case study.** The
  strongest asset available, and it already exists: dozens of dashboards,
  measurable impact, plus enablement. Get written permission, anonymize if
  needed, write real before/after numbers. Move that client onto a formal
  retainer under the BaseBloom name if they aren't already.
- **Week 7 — Price and paper the offer.** Publish a Data ladder mirroring the
  web ladder's shape — one-time build plus monthly care — because that shape
  already converts for this business. Write the SOW template, the discovery
  questionnaire, and a **data-readiness checklist built around the qualifying
  question in §1**, so bad fits are disqualified before a fixed price is quoted.
- **Week 8 — Sell.** Offer a free dashboard audit to every care-plan client and
  to the warm network. The free-demo motion is already the proven BaseBloom sales
  mechanic (`index.html:436`) — reuse it rather than inventing one. Also: call
  five existing clients and ask directly what they'd pay. There is no defensible
  public data on SMB willingness-to-pay for embedded dashboards; five phone calls
  beat any amount of further research.

### Days 61–90 — Deliver, systematize, decide

Goal: one Tier 2 engagement delivered and repeatable, with evidence for whether
to double down.

- **Weeks 9–10 — Deliver the first engagement**, and instrument the delivery:
  track actual hours against the quoted price. The first engagement's real job is
  to tell you whether the price is right.
- **Week 11 — Systematize.** Semantic-model starter, a visual/theme kit matching
  the BaseBloom palette (ink `#101C13`, bloom green `#16B364`, sand `#D8C6A0`,
  brown `#C89253`), a refresh-monitoring runbook, a client onboarding checklist.
  Add **enablement training as a productized SKU** — already done successfully
  once, high-margin, low-delivery-risk, and it does not scale with your hours the
  way builds do.
- **Week 12 — Review against pre-committed numbers.** Set the targets in week 0
  so the review is honest rather than retrospective: Tier 2 conversations held,
  engagements signed, realized hourly rate, MRR added. Decide explicitly —
  expand Data, hold it as an attach-on, or stop.

### Suggested price ladder (verify against §6 before publishing)

| SKU | Price | Notes |
|---|---|---|
| Monthly report | included in care plan | Tier 1. Retention, not revenue. |
| Dashboard build | $2,000–$5,000 | ~15–30 hrs at $150–$225/hr. |
| Data care plan | $300–$800/mo | Or $150–$400 bundled into an existing site retainer. |
| Pipeline / automation build | day rate, ~$1,200–$1,600 | The refresh-chain work. |
| Team enablement | fixed per cohort | Highest margin, already proven. |

Benchmarks behind this: senior US independents transact at **$150–$225/hr** —
ignore the $56–$87 marketplace averages, which are a different (offshore/
commodity) market. SMB dashboard builds land **$1,500–$5,000**; maintenance
retainers **$300–$1,500/mo**. Note the anchor you're arguing against: agency
reporting *tools* are priced at $20–$80/mo, so lead with the build and the
interpretation, never with "a dashboard."

---

## 4 · Additional best practices

**Sell the pipeline, not the pictures.** Dashboards are the visible 20%. The
defensible, retainer-generating work is the refresh chain — the source-to-visual
automation you already build. Describe and price the plumbing, or clients anchor
on "it's just a chart" and compare against a $9/month tool.

**Every dashboard is a subscription by construction.** Websites decay slowly;
dashboards break loudly the moment a source schema changes. That's a feature of
the business model — monitoring, alerting and refresh SLAs are legitimately worth
a monthly fee. Never sell a dashboard without an attached care plan; an
unmaintained dashboard is a liability that will eventually be blamed on you.

**Sell the alert, not just the dashboard.** An SMB owner will not log in daily.
A Power Automate / Data Activator threshold alert — "job margin dropped below X"
— arriving by email or text is often worth more to them than the dashboard, and
it is far cheaper to run.

**Refuse a claim, again.** The strongest line on the current site is *"No ranking
promises"*; the hero audit specifically credits it for differentiating by
*refusing* a claim competitors make. The data equivalent: **no insights without
data to back them.** Say plainly that if the data isn't there you'll say so
rather than build a pretty dashboard on nothing. It disqualifies bad fits and is
the most trust-building sentence available in this category.

**Do not fabricate the demo.** The site's own source comment sets the standard.
Fake dashboard numbers are more corrosive than fake testimonials, because the
buyer is specifically purchasing numerical honesty.

**Watch the brand tension.** "Websites for local trades · Atlanta, GA" is tightly
targeted, and that tightness is why it works. Generic BI consulting can dilute
it. Keep trades as the front door; let Data live as a separate section and, if it
grows, a separate landing page — not a rewritten hero.

**Keep the day job clean.** No client data, tooling, licenses, devices or hours
crossing between employer and BaseBloom. Cheap to maintain from day one,
expensive to untangle later.

---

## 5 · Verification

- **Reporting is honest:** generate the Tier 1 report for a real client and
  reconcile every metric by hand against the GBP and analytics consoles. Confirm
  the page renders correctly at 390px.
- **Embedding works:** load the demo dashboard signed-out in a private window;
  confirm no license prompt, and measure load on throttled 4G. If it's
  unacceptably slow on a phone, the static path wins for that use case.
- **Isolation works:** with two test tenants, confirm tenant A's token cannot
  read tenant B's rows. Do this before the second client, not after.
- **Cost is bounded:** confirm capacity actually suspends on schedule; check the
  first full billing cycle against estimate; set a spend alert.
- **The site doesn't regress:** re-run the audit's contrast sampler
  (`docs/basebloom-hero-audit/contrast-sampler.mjs`) and re-measure LCP/CLS after
  adding analytics and any new section. Current baseline: desktop LCP 1080ms /
  CLS 0, mobile LCP 428ms / CLS 0.0531. The dashboard route must not touch these.

## 6 · Open items, highest priority first

1. **Does F2 actually support app-owns-data embedding for unlimited external
   viewers, or does an F64 threshold apply?** Sources conflicted, and the
   conflation appears to be between *organizational consumption in the Power BI
   service* (where the F64 rule is real) and *app-owns-data embedding* (where it
   should not apply). This is a ~$156/mo vs ~$8,400/mo question. Verify at
   `learn.microsoft.com/power-bi/developer/embedded/embedded-capacity` and
   `learn.microsoft.com/fabric/enterprise/licenses`, or with a Microsoft partner.
   **Do not publish Data pricing before this is settled.**
2. **Re-verify all pricing** against the Azure pricing calculator directly. None
   of the figures in this plan came from a primary source.
3. **Real F2 performance under embedded load** — no benchmark data exists. A
   two-week PAYG trial with a representative model is the only way to know.
4. **Day-90 target numbers** — David to set, in week 0.
5. **Case study consent** from the existing BI client.
6. **Entity status** — LLC or sole proprietorship, and the footer corrected to match.
