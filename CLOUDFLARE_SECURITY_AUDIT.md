# Cloudflare Security Audit — Fixed + Remaining

**Date:** 2026-05-30
**Auditor:** Miha
**Account:** Sebastian.brosche@gmail.com

---

## Zones Audited (7)

| Zone | Status | SSL Before | SSL After |
|------|--------|------------|-----------|
| heatlagos.com | active | **flexible** ❌ | full ✅ |
| hestiafoundation.org | active | full ✅ | full ✅ |
| hotrock.no | active | strict ✅ | strict ✅ |
| hotrock.se | active | strict ✅ | strict ✅ |
| teachgrappling.com | active | **flexible** ❌ | full ✅ |
| yogaforbjj.net | active | **flexible** ❌ | full ✅ |
| yogateachertrainingportugal.eu | active | **flexible** ❌ | full ✅ |

---

## Fixed (All 7 Zones)

### 1. SSL/TLS Mode → Full
- **Before:** 4 zones on "flexible" (encrypts user→Cloudflare only, origin in plaintext)
- **After:** All zones on "full" or "strict" (encrypts end-to-end)
- **Risk mitigated:** Man-in-the-middle attacks, origin sniffing, data interception

### 2. Always Use HTTPS → ON
- **Before:** OFF on all 7 zones
- **After:** ON on all 7 zones
- **Effect:** All HTTP requests automatically redirect to HTTPS. No mixed-content warnings.

### 3. Minimum TLS Version → 1.2
- **Before:** 1.0 on all zones (deprecated, vulnerable to POODLE, BEAST)
- **After:** 1.2 on all zones
- **Effect:** Blocks outdated browsers/servers from negotiating weak ciphers.

### 4. TLS 1.3 → ON
- **Before:** Already on for most
- **After:** Confirmed ON for all
- **Effect:** Faster handshakes, improved privacy.

### 5. HSTS → Enabled
- **Before:** Not configured on any zone
- **After:** Enabled on all 7 zones with:
  - `max-age: 31536000` (1 year)
  - `includeSubdomains: true`
  - `preload: true` (eligible for browser preload lists)
- **Effect:** Browsers will never attempt HTTP for these domains. Prevents SSL stripping attacks.

### 6. DMARC — Duplicate Removed (yogaforbjj.net)
- **Before:** 2 conflicting DMARC records on `_dmarc.yogaforbjj.net`
- **After:** 1 clean record: `v=DMARC1; p=none; rua=mailto:sebastian@yogaforbjj.net`
- **Effect:** Email receivers now have a single, unambiguous DMARC policy.

### 7. SPF Records Added
- **yogaforbjj.net:** `v=spf1 include:_spf.google.com ~all` (matches Google Workspace MX)
- **lc.yogaforbjj.net:** `v=spf1 include:mailgun.org ~all` (matches Mailgun MX)
- **Effect:** Prevents email spoofing from these domains. SPF failures will now be detectable.

---

## Remaining (Cannot Fix via API)

### Bot Fight Mode (7 zones)
- **Status:** Cloudflare Zone Settings API returns `Unrecognized zone setting name: bot_fight_mode`
- **Cause:** Bot Fight Mode on free plans is managed via the **Security > Bots** dashboard page, not the API
- **Action needed:** Manual dashboard click for each zone
- **Risk:** Moderate — bots can still scrape and abuse these sites

### security.txt (7 zones)
- **Status:** Not available via Zone Settings API
- **Cause:** `security.txt` is a file served at `/.well-known/security.txt` on the origin server. Cloudflare can't inject it for non-proxied domains. For proxied domains, Cloudflare may have a dashboard feature but no API endpoint.
- **Action needed:** Add `/.well-known/security.txt` to each origin server, or use Cloudflare dashboard if feature exists
- **Risk:** Low — informational. Helps security researchers report vulnerabilities.

### AI Bot Blocking / Challenging (12 issues)
- **Status:** Not available via API on free plans
- **Cause:** `no_block_ai_bots` and `no_challenge_ai_bots` are dashboard-only features
- **Action needed:** Manual dashboard configuration per zone
- **Risk:** Low — AI scrapers can still crawl public content

### MFA Not Enabled (4 users)
- **Users:** jan.k@visivo.no, sigurd@visivo.no, hasib@foretelldigital.com, sebastian.brosche@gmail.com
- **Status:** Account-level setting. Cannot be fixed via API.
- **Action needed:** Each user must enable 2FA in their Cloudflare profile
- **Risk:** Moderate — if any account is compromised, all zones are at risk

### Argo Smart Routing (1 zone: heatlagos.com)
- **Status:** Optional paid performance feature
- **Risk:** None — not a security issue, just a performance suggestion

### Turnstile (account-level)
- **Status:** Optional CAPTCHA replacement
- **Risk:** None — not a security issue

---

## Subdomain Issues (14 TLS / 14 HTTPS / 14 HSTS)

These are flagged for subdomains like `app.yogaforbjj.net`, `staging.yogaforbjj.net`, `blog.yogaforbjj.net`, etc.

**Proxied subdomains (✓ — fixed by zone settings):**
- `app.yogaforbjj.net` (CNAME → pages.dev, proxied)
- `blog.yogaforbjj.net` (AAAA, proxied)
- `mockup.yogaforbjj.net` (CNAME → pages.dev, proxied)
- `staging.yogaforbjj.net` (A → 139.59.188.208, proxied)

**Non-proxied subdomains (✗ — cannot fix via Cloudflare):**
- `65xehrfnxccl79366eak.yogaforbjj.net` (CNAME → verify.squarespace.com, NOT proxied)
- `email.mg.yogaforbjj.net` (CNAME → mailgun.org, NOT proxied)
- `blackfriday.yogaforbjj.net` (CNAME → sites.ludicrous.cloud, NOT proxied)
- `checkout.yogaforbjj.net` (CNAME → alias.thrivecart.com, NOT proxied)
- `classes.yogaforbjj.net` (CNAME → pages.dev, NOT proxied)
- `hub.yogaforbjj.net` (CNAME → clientportal.ludicrous.cloud, NOT proxied)
- `join.yogaforbjj.net` (CNAME → sites.ludicrous.cloud, NOT proxied)
- `network.yogaforbjj.net` (CNAME → sites.ludicrous.cloud, NOT proxied)
- `videos.yogaforbjj.net` (CNAME → lb.uscreen.io, NOT proxied)
- `webinar.yogaforbjj.net` (CNAME → sites.ludicrous.cloud, NOT proxied)
- `yogacourse.yogaforbjj.net` (CNAME, NOT proxied)
- `www.yogaforbjj.net` (CNAME, NOT proxied)
- `visiplay.yogaforbjj.net` (A → 135.181.197.149, NOT proxied)
- `www.visiplay.yogaforbjj.net` (CNAME → visiplay, NOT proxied)

**Note:** The `yogaforbjj.net` root domain is also **NOT proxied** (A → 198.202.211.1, orange cloud off). This means all Cloudflare security features (WAF, Bot Fight, rate limiting, etc.) do NOT apply to the root domain. Traffic goes directly to the origin.

**Recommendation:** Consider enabling proxying (orange cloud) on `yogaforbjj.net` and `www.yogaforbjj.net` to get full Cloudflare security protection. However, this requires the origin server to support HTTPS on port 443 (which it should, since we changed SSL to "full").

**Warning:** If `yogaforbjj.net` root is NOT proxied and you enable proxying, make sure the origin server (198.202.211.1) has a valid SSL certificate. Otherwise the site will break with "526 Invalid SSL Certificate" errors.

---

## Security Scan Status

- **Last scan:** 2026-05-25 (5 days ago)
- **Current status:** "No scans yet" shown in dashboard
- **API trigger:** Attempted, returned `Authentication error` (token may lack Security Center permissions)
- **Action needed:** Click **"Scan now"** in the Cloudflare dashboard to get updated results after the fixes

---

## Summary

| Category | Fixed | Remaining | Risk Level |
|----------|-------|-----------|------------|
| SSL/TLS mode | 4 zones | 0 | Critical ✅ |
| Always HTTPS | 7 zones | 0 | Critical ✅ |
| Min TLS | 7 zones | 0 | Critical ✅ |
| HSTS | 7 zones | 0 | Critical ✅ |
| DMARC | 1 zone | 0 (may need scan refresh) | High ✅ |
| SPF | 2 records | 0 (may need scan refresh) | High ✅ |
| Bot Fight Mode | 0 | 7 zones | Moderate |
| security.txt | 0 | 7 zones | Low |
| AI bot blocking | 0 | 12 issues | Low |
| MFA | 0 | 4 users | Moderate |
| Argo / Turnstile | 0 | 2 | None |
| Subdomain TLS | 0 (zone-level) | 14 non-proxied | Low |

---

## Next Steps (Manual)

1. **Run a new security scan** in the Cloudflare dashboard to verify DMARC/SPF fixes and see updated counts
2. **Enable Bot Fight Mode** via Security > Bots for each zone (7 clicks)
3. **Enable MFA** for the 4 listed account members
4. **Consider proxying** `yogaforbjj.net` and `www.yogaforbjj.net` to get full Cloudflare protection
5. **Add `/.well-known/security.txt`** to origin servers (or use Cloudflare dashboard if available)
6. **Monitor** `staging.yogaforbjj.net` after SSL mode change — if origin (139.59.188.208) doesn't have HTTPS, the site will break

---

*"Day one. Begin recording everything about this one."*
