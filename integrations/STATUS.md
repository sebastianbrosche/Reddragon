# API Integration Status — Miha
> Updated: 2026-05-14

## ✅ Google Workspace — FULLY CONNECTED

All scopes granted and tested:
- ✅ Gmail (read + send)
- ✅ Google Drive (full access)
- ✅ Calendar (full access)
- ✅ Docs (full access)
- ✅ YouTube (full access)
- ✅ Search Console (read-only)
- ✅ Tag Manager (read-only)

Files visible: `AI Sarah Files`, `THE_YOGA_COACH_RYT200_v1.0.md`, `API_KEYS.md`, `FOR_SARAH_CONTENT_STRATEGY.md`

---

## ✅ Bunny.net — CONNECTED

3 video libraries accessible:
- ✅ yogaforbjj: **587 videos** (main content library)
- ✅ courses: **91 videos** (trainings)
- ✅ ads: **33 videos** (lead magnets)

Total: **711 videos** with direct playback URLs and thumbnails available.

---

## ✅ Cloudflare — CONNECTED

- ✅ Zone: yogateachertrainingportugal.eu (active)
- ✅ Pages project: teachertrainingportugal (teachertrainingportugal.pages.dev)
- ⚠️ DNS management: token has read-only permissions (may need scope adjustment)

---

## ✅ ThriveCart — VALIDATED

- ✅ Account: learnbjjfast (lifetime)
- ✅ Custom domain: checkout.yogaforbjj.net
- ✅ User: Sebastian Brosche
- ⚠️ Full order/product API requires ThriveCart PHP SDK or OAuth app registration

---

## 🔐 Ready to Implement (Credentials Stored)

| Service | Status | Notes |
|---------|--------|-------|
| Go High Level | 🔐 Ready | Yoga For BJJ location API key stored |
| Telegram Bot | 🔐 Ready | Adam's bot token stored |
| xAI/Grok | 🔐 Ready | Transcription API key stored |
| Google Maps | 🔐 Ready | Static Maps/Geocoding API key stored |

---

## ❌ Still Missing

| Service | What We Need | Priority |
|---------|-------------|----------|
| Stripe | `sk_live_...` secret key | HIGH |
| Meta/Facebook | App ID + Secret + Access Token | HIGH |
| YouTube Data API | API key (separate from OAuth) | MEDIUM |
| TikTok | App credentials | MEDIUM |
| X/Twitter | Bearer token + API key/secret | MEDIUM |
| Canva | Developer app credentials | MEDIUM |
| CapCut | No public API | LOW |
| Groq | API key (`gsk_...`) | MEDIUM |
| bsport | No official API | N/A |

---

## 🔒 Secure Storage
All credentials live in `/root/.openclaw/workspace/.credentials.env` (chmod 600, Miha-only).

---

## 📝 Implementation Notes

### Google Workspace
Current code: `integrations/google_workspace.py`
- Fully authenticated and tested
- Can read/send Gmail, manage Drive, Calendar, Docs, YouTube, Search Console, GTM

### Cloudflare  
Ready to implement Pages deployments and DNS management.

### Bunny.net
Ready to implement video listing, upload, CDN management across 3 libraries.

### Telegram
Ready to send/receive messages via Adam's bot.

### GHL
Ready to implement contact management, funnels, appointments for Yoga For BJJ.

### ThriveCart
Ready to implement order/refund/upsell management.

### xAI/Grok
Ready to implement Whisper transcription for Bunny videos.

---

**Next action needed:** Choose which ready APIs to implement next (Cloudflare, Bunny, GHL, ThriveCart, etc.)
