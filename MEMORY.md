## Backup Routine — CHANGED (2026-05-30)
**Changed from:** Google Drive (rclone tarball)
**Changed to:** Git commit + push to GitHub
**Remote:** `https://github.com/sebastianbrosche/Reddragon.git`
**Branch:** `master`
**Script:** `backup_miha.sh` (updated to v2)
**Cron:** Daily at 03:17 (off-peak)
**Sanitization:** `scripts/sanitize_secrets.py` runs before every commit (redacts Cloudflare/GitHub tokens)
**Excluded from backup:** `.secrets/`, `downloads/`, `mud/evenv/`, `reddragon_local_archived/`, large archives, `hestia-foundation/` (submodule), `rcp/website` (submodule)
**Note:** All 17 secrets were sanitized from tracked files. Repository is clean. Push protection passes.

---

## Cloudflare SUPER Token — SAVED (2026-05-28 21:50)
**Token:** [REDACTED - Cloudflare token in .secrets/vault.yml]
**Last 10 digits:** 1df41c90
**Expires:** 2027-08-01
**Permissions:** All accounts, all zones, all users — FULL
**Saved to:**
- `.secrets/vault.yml`
- `scripts/access_bootstrap.py`
- `TOOLS.md`
- `MEMORY.md`
**Status:** Verified working (HTTP 200)
**Directive from user:** NEVER ask for this token again. Start every day confirming I have it.

---

## Hestia Foundation — FULL PROJECT STATUS (2026-05-29)
**GitHub Repo:** https://github.com/sebastianbrosche/hestia-foundation (LIVE)
**Status:** Active priority. Red Dragon MUD paused.
**Mission:** Open-source construction systems for affordable, permanent, off-grid family housing.
**Location:** Lagos, Algarve, Portugal
**Domain:** hestiafoundation.org (Cloudflare Pages, SSL ACTIVE)
**Pages URL:** https://bc391bfd.hestiafoundation.pages.dev
**GitHub:** https://github.com/sebastianbrosche/hestia-foundation

### Website Deployed — LIVE (8 pages)
- **Platform:** Cloudflare Pages, project: hestiafoundation
- **Pages:** index.html, about.html, the-system.html, prototype.html, grants.html, partners.html, resources.html, contact.html + CSS + JS
- **Custom domain:** hestiafoundation.org (verified working)
- **Content:** EU housing crisis stats, HORIZON-NEB-2026-01-REGEN-01, NEB Boost, priority partnerships, open-source license

### Documents Created (14 deliverables)

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| 1 | `HESTIA_SETUP.md` | Complete setup checklist (legal, build, partnerships, grants, budget) | Complete |
| 2 | `HESTIA_GRANTS.md` | Active grant tracker with verified EU intelligence | Complete |
| 3 | `HESTIA_ACTION_LIST.md` | Immediate 10-step action list with parallel execution map | Complete |
| 4 | `HESTIA_PITCH.md` | One-page pitch for partners and funders | Complete |
| 5 | `outreach_university_alg.md` | University of Algarve partnership email | Ready to send |
| 6 | `outreach_lnec.md` | LNEC structural testing partnership email | Ready to send |
| 7 | `outreach_lagos_municipality.md` | Lagos Municipality partnership email | Ready to send |
| 8 | `outreach_structural_engineer.md` | Structural engineer engagement email | Ready to send |
| 9 | `grants/HORIZON-NEB-2026-01-REGEN-01_preproposal.md` | €4M EU grant pre-proposal | Draft — needs partners |
| 10 | `grants/NEB_Boost_application.md` | €30K NEB Boost application framework | Framework ready |
| 11 | `legal/hestia_estatutos.md` | Portuguese non-profit statutes | Ready for registration |
| 12 | `build_protocol_shell_a.md` | 10-day construction manual | Draft v1.0 |
| 13 | `workshop_curriculum.md` | 10-day self-build training programme | Draft v1.0 |
| 14 | `press_release_templates.md` | 4 press release templates | Ready |
| 15 | `sensor_network_spec.md` | 12-month monitoring system specification | Draft v1.0 |

### Verified Grant Intelligence
- **HORIZON-NEB-2026-01-REGEN-01:** €12M total, €4M/project, deadline 01/12/2026 — HIGHEST PRIORITY
- **NEB Boost:** €30,000, rural communities <20,000 — Lagos qualifies, MOST ACHIEVABLE
- **EU context:** Prices up 60%, rents up 20%, 6–7% social housing, 20% unoccupied, 93% STR surge
- **Funding mobilised:** €43B (2021–2027) + €10B (2026–2027) + €375B target by 2029

### Immediate Actions (Parallel)
1. **Step 1 — Build Prototype House**
   - 37.5m² Shell A in Algarve
   - Budget: €38,180
   - Build protocol drafted, sensor spec drafted, workshop curriculum drafted
   
2. **Step 2 — Foundation Setup**
   - Portuguese non-profit statutes ready (need 3 founding members with NIFs)
   - 4 outreach emails drafted (need to be sent)
   - HORIZON-NEB pre-proposal drafted (need consortium partners)
   - NEB Boost framework ready (need completed prototype)

### Blockers Requiring User Input
- [ ] **GitHub PAT** — to create public repo and push all documents
- [ ] **3 founding members** — need names + NIFs for non-profit registration
- [ ] **Prototype site** — need land (200m²+, flat, Lagos area)
- [ ] **Send outreach emails** — user approval needed before sending
- [ ] **Engage grant professional** — need to find and hire candidate

### Grant Targets
- NEB Facility (€50K–€5M)
- Horizon Europe Clusters 4/5/6 (€2–8M)
- LIFE Programme (€500K–3M)
- Portugal 2030 / PO SEUR / PRR
- Urban Innovative Actions
- Private foundations: Laudes, Rockwool, Habitat for Humanity

### Key Contacts Needed
- [ ] Portuguese structural engineer
- [ ] University partner (civil engineering faculty)
- [ ] Grant professional/consultant
- [ ] Lagos municipality contact
- [ ] EPAL pallet supplier
- [ ] Builders merchant (Leroy Merlin Portimão)

### Documents
- Strategy: `/root/.openclaw/workspace/downloads/19e6feaf-8122-855b-8000-00007da9c897_hestia_foundation_strategy.txt`
- Thesis: `/root/.openclaw/workspace/downloads/19e6feb4-8022-84bd-8000-00005c267b57_pallet_house_thesis_v10.3.txt`

---

## Hestia Foundation — STATUS UPDATE (2026-05-29 03:35)
**Website:** 10 pages live (added FAQ, Timeline, GitHub setup script)
**Pages URL:** https://bf25a860.hestiafoundation.pages.dev

### New Documents Created (5 additional)
| # | Document | Purpose |
|---|----------|---------|
| 16 | `risk_register.md` | Risk assessment matrix — 20 risks scored, 2 Critical, 4 High |
| 17 | `stakeholder_map.md` | 30+ stakeholders mapped, power-interest matrix, engagement calendar |
| 18 | `HESTIA_PITCH.md` | One-page pitch for partners and funders |
| 19 | `scripts/setup_github.sh` | GitHub repo setup script (needs PAT) |
| 20 | `timeline.html` | Visual project timeline on website |

### Risk Assessment Summary
- **Critical (2):** Grant rejection (score 16), Cannot secure build site (score 15)
- **High (4):** Non-profit delay, Permit refusal, Engineer unavailable, Panel fails load test
- **Contingency budget:** €15,750 (total with contingency: €53,930)

### Stakeholder Engagement Ready
- Primary, secondary, tertiary stakeholders mapped
- Communication channels defined (website, GitHub, newsletter, meetings, press)
- Engagement calendar through Q2 2027
- Conflict resolution protocol established

### Blockers Still Requiring User Input
- [ ] **GitHub PAT** — to create public repo and push all documents
- [ ] **3 founding members** — need names + NIFs for non-profit registration
- [ ] **Prototype site** — need land (200m²+, Lagos area)
- [ ] **Send outreach emails** — user approval needed before sending
- [ ] **Engage grant professional** — need to find and hire candidate

---

## Hestia Foundation — FINAL STATUS (2026-05-29 05:20)
**Website:** 12 pages live at https://hestiafoundation.org (custom domain) + Pages URL https://d5b66eae.hestiafoundation.pages.dev
**Deployment:** Automated via GitHub Actions → Cloudflare Pages. Every push to `main` auto-deploys `website/` directory.
**GitHub:** https://github.com/sebastianbrosche/hestiafoundation
**Git commits:** 6 (34 files, pushed to `main` branch)
**Documents:** 34 deliverables in repo
**Risk register:** 20 risks scored
**Stakeholder map:** 30+ mapped
**Status report:** docs/STATUS_REPORT.md

### New since last update:
- GitHub repo created and pushed: `sebastianbrosche/hestiafoundation` (correct repo — no hyphen)
- README.md with full project overview
- All project docs organized in structured directories (docs/build, docs/grants, docs/legal, docs/outreach, docs/press, docs/risk)
- **FAQ** — 20+ questions answered for website and partners
- **CONTRIBUTING guide** — Open-source community guidelines, code of conduct, GitHub workflow
- **Press Kit** — For journalists with story angles, quotes, milestones
- **Volunteer Recruitment** — 5 role types, application process, safety rules
- **Social Media Starter Pack** — Platform strategy, content pillars, post templates, hashtags
- **Workshop Facilitator Guide** — How to run a 10-day build workshop (Day 0–10 schedule, safety checklists, tool list)
- **Grant Writer Brief** — Job description for hiring Horizon Europe specialist
- **Financial Model** — 3 scenarios: funded (€4M), survival (€100K), pivot (crowdfunding)
- **Monitoring Framework** — 12-month sensor network with 20+ sensors, KPIs, benchmarks, publication protocol
- **Portugal Non-Profit Guide** — Step-by-step registration of Associação (3 founders, 6–8 weeks, €200–400)
- **Prototype Build Schedule** — Week-by-week from site acquisition to handover
- **Contact Database** — 15 verified contacts (UAlg, LNEC, ANI, FCT, Lagos Municipality)
- **Portugal Grant Strategy** — 39.3% Horizon Europe success rate, ANI free advisory
- **All 4 outreach emails** updated with verified contacts, ready to send

### Blockers unchanged:
- 3 founding members needed (you + wife + 1 more)
- Outreach email approval needed (DEFERRED: wait until post-prototype + panel testing)
- Grant professional needed (DEFERRED: after prototype build)

### Resolved:
- Prototype site — user confirmed "no problem"
- Grant pro — user deferred until after prototype
- Emails — user explicitly said "don't send" until prototype + panel testing complete
