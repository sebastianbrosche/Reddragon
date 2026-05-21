Heat Lagos, API & Access Keys

Managed by: Miha (backed up, protected, version-controlled)
Last updated: 16 May 2026
Rule: ONE doc, updated in place, never duplicated

---

SERPAPI

Key: fe991cba4526642095747280988f8e326ba9c9056bed1d15867bc36f91120a2d
URL: https://serpapi.com/manage-api-key
Owner: Sebastian (account holder)
Access: All team members (read only, Miha holds the key doc)

Capabilities we care about:
- Google Search API
- Google Local API (find gyms, wellness centers in Algarve)
- Google Maps API (competitor locations, reviews)
- Google Reviews API (competitor analysis)
- Google Trends API (wellness trends in Portugal)
- Google Jobs API (personal trainer hiring)
- YouTube Search API (content research)
- YouTube Video Transcript API (HUGE, pull transcripts from any video)
- Google Hotels API (wellness tourist research)
- Google Images API (content inspiration)

NOTES:
- Rate limits apply, use responsibly
- Prefer cached results when possible
- Document what we search for in the Search Log sheet

---

SHELLY (Smart Home / Sauna Controls)

API access: VERIFIED and WORKING
Server: https://shelly-258-eu.shelly.cloud
Auth Key: NDE0MjVjdWlkF8CEE62AA4EEA592AF52DFDF3421D60EB3FD9E65E959A5C942145E99B80B0166295492AACF96A771
Status: Active, tested by Kimi and Miha
Current reading: 5.27 kW total (two sauna heaters running, 66C and 78C, 7 devices total)
NOTE: STOP all Shelly work per Sebastian. It's running, forget about it.

---

BSPORT

API: None available
Access: Dashboard login only
Owner: Sebastian (account holder)

STAFF login (for class management, changes, backoffice):
  - URL: https://backoffice.bsport.io/
  - Email: adambot@yogaforbjj.net
  - Password: kimiclaw321
  - Actions: make changes Sebastian explicitly requests (substitute teachers, class updates, etc.)
  - NOTE: Only make changes when Sebastian explicitly asks. Otherwise read-only.

CLIENT login (for booking, testing user experience):
  - URL: https://heatlagos.com/
  - Email: adam@yogaforbjj.net
  - Password: kimiclaw321
  - Actions: view class bookings, check email campaigns, test user experience
  - NOTE: Do NOT make changes without explicit permission

---

GOOGLE WORKSPACE / GMAIL API

Status: Connected (Adam set up OAuth)
Owner: Sebastian
Access: Adam (for email campaigns if bsport fails)
Use: Summer membership push to 234 leads

---

CLOUDFLARE

Status: Active (YTT site hosted)
Owner: Sebastian
Access: Adam (website management)
Sites:
  - yogateachertrainingportugal.eu
API Token needed: [SEBASTIAN TO PROVIDE - PASTE IN TEXT]

---

META / FACEBOOK / INSTAGRAM

Status: Stine runs @heat_lagos Instagram
Owner: Stine (Sebastian's wife)
Access: Read only for team (learn her style, repurpose content)
Action: We need to review her posts to understand the visual style

---

YOUTUBE

Access: Via SerpAPI YouTube Video Transcript API
Capability: Paste any YouTube URL, pull transcript automatically
Use case:
  - Sebastian sees a good video
  - Pastes URL in chat
  - Team pulls transcript
  - Extracts valuable points
  - Adds to document or creates blog post

---

TIDYCAL

API Key: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNzZkOTVjZGM4M2VmYTAxMDI3YzJkM2Y1MTlhNDAzMDNkZjkzMmI5YWZmYTYxYzhhOTFhNTVlYWU5YTIxZTFmMDNiOGRkMmM5ZWEzZjgxMTgiLCJpYXQiOjE3Nzg5MjU2MTMuMzkyNzM1LCJuYmYiOjE3Nzg5MjU2MTMuMzkyNzM3LCJleHAiOjQ5MzQ1OTkyMTMuMzgzMjQ1LCJzdWIiOiIxMDgyOTAiLCJzY29wZXMiOltdfQ.gro-_tvHkFiuljae6MIhK4yGzvIxOntmdL3Y0OEldBhNKWPQpWuXKbjR6kdmWVNu_305WaOGwfWZrb1PeL8MIMU9Go1k5lbv-lEy59iDM1dWXGATcylFh-p9AKYDRtILNRwBj8ze76_8y6ie8aW30n3KomVPSwl3GtOLrnypj0U5JcgUZq2muNEPpCkawzCx4OuA4za5PRIAm_ZBhdRgw7U0BT8i08cYAONLg_jQEgR2kcsn6iS-xugyed_CIp_ksu6CKhqbwlFv_dMkDroeuOkA5FgQ9SUTIYPSngs13CN-ipSM3hwQ47MV3kLWdl_uT81-baYIuzvLbrVIUh5Ttu7u2qPxzMQzHZp9dHRsfRAO3EooS61EmsEm2rjOhbbWQTPaRf5rl1Rnt6H0rKH25NGBW_7JmPXMA5ZnVmeifOB6mNya8uqgeco6iOGoqWMwfs-NTmqv3PVbXqySAEDKbzKd4ijHtQQizObdJtsL4kVEd3IbxoYKO-DZiifffxttgN1lwMornxSQy6LXDgP0GzvRQaKxqdOG_FlycEEV-BZI5ZyicdO8Zbr5dBV1H33MHQSEiKqk3wIZsNcVUumXBDC0n39epKPrfNuUzI8zpxmzhZie5tvWPnwhvklnbV236LaeaPT2zVraRUwbZGsuIvRR0-R8NdzjfACxmvt1Kxw
Owner: Sebastian
Added: 16 May 2026
Status: Pending verification (Sarah to test)
Purpose: Schedule onboarding / followup personal calls and coaching inside the pipeline

---

OTHER APIs NEEDED

Google Home / Alexa integration:
  - Research needed: open-source or API-accessible voice assistant
  - Goal: Voice commands to Shelly (sauna controls)
  - Assigned: Sarah or Adam to investigate

Canva API:
  - For automated image generation
  - Research if available

Groq / Whisper:
  - For voice transcription (Sebastian's voice messages)
  - Already known to team

---

ACCESS LOG

| Date | Who | What API | Purpose | Result |
|------|-----|----------|---------|--------|
| 16 May | Sebastian | TidyCal | API key received for onboarding scheduling | Pending Sarah verification |
| 14 May | Kimi | SerpAPI | Set up team access | Key added |
| 14 May | Adam | bsport | Summer email campaign | OAuth connected, API blocked |
| 14 May | Adam | Gmail | Fallback for 234 leads | OAuth connected |
| 14 May | Adam | Cloudflare | YTT site hosting | Active, token pending |
| 14 May | Sebastian | bsport | New login credentials | adam@yogaforbjj.net / kimiclaw321 |
| 14 May | Kimi | SerpAPI | Google Maps testimonials | 8 reviews pulled, 5.0 rating |
| 14 May | Kimi | Shelly | Test sauna power | 5.27 kW verified |
| 14 May | Sebastian | bsport | Corrected logins with staff/client URLs | adambot@yogaforbjj.net (staff), adam@yogaforbjj.net (client) |

---

SECURITY RULES

1. This doc lives in ONE place, managed by Miha
2. Never share keys in chat (only the key doc)
3. Never create a second version of this doc
4. Update in place when new keys arrive
5. If a key is compromised, rotate immediately and update this doc
6. Team members check this doc regularly for new access
7. Sebastian is installing Chromium browser for shared bot access

---

NEXT ADDITIONS

- Cloudflare API token (Sebastian says Adam should have it from yesterday; if not found, new one to be created)
- Meta/Instagram business account access (if needed for ads)
- Canva API (if available)
- TikTok API (if needed for content)
