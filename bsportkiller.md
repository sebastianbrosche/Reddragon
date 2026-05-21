# bsportkiller.md — The Complete bsport Dashboard Guide

> **Status:** Documentation phase COMPLETE. Standing by for Adam's questions.
> **Researcher:** Miha (documentation + support)
> **Explorer:** Adam (hands-on testing)
> **Directive:** Sebastian
> **Deliverables:**
> - `bsport_help_center.pdf` — 233 articles, 667KB, full help center compilation
> - `bsport_quick_start.pdf` — 2-page cheat sheet, 123KB, essentials only
> - Both sent to group chat above.

---

## Quick Reference

| Item | Value |
|------|-------|
| Backoffice URL | https://backoffice.bsport.io/login |
| Client Portal | https://heatlagos.com (for members) |
| Support Hours | Weekdays 8AM–5PM only |
| API Type | Token-based (extract from browser network requests) |
| Known Logins | Staff: adambot@yogaforbjj.net / kimiclaw321 (backoffice.bsport.io) |
| | Client: adam@yogaforbjj.net / kimiclaw321 (heatlagos.com) |

---

## What bsport Is

bsport is a SaaS platform for fitness/yoga studios. It's feature-heavy and modular — studios pay per feature, not flat rate. Built for multi-location studios that want marketing automation, CRM, and booking all in one.

**Key positioning:**
- Target: High-end sports clubs, yoga studios, dance schools, fitness centers
- ~150 custom iOS/Android apps deployed
- 800+ partners using the backoffice
- Modular pricing (from ~€150/mo per feature, excluding VAT)
- Annual contracts with 2-month cancellation notice

---

## Member-Facing Interface (from Yogama Tutorial)

bsport has both a **member portal** (what clients see) and a **studio backoffice** (what staff see). Here's what the member side looks like — this helps understand the full flow:

### Member Login
- URL: https://backoffice.bsport.io/login
- Members use their email as username
- Can reset password via "mot de passe oublié" (forgot password)

### Member Dashboard Sections (from tutorial screenshots)
1. **Calendar/Planning** — Shows available classes by date
2. **My Space / Profile** — Personal info, memberships, history
3. **Cart** — Add passes, pay online or "pay later" (payer plus tard)
4. **History** — Past and upcoming bookings, with cancel option
5. **Subscriptions** — Active memberships, renewal dates

### Member Actions (step-by-step from Yogama)

**Creating an Account:**
- Go to backoffice.bsport.io/login
- Enter email + create password
- Or click "forgot password" if account exists but password lost

**Buying a Pass/Course Card:**
1. Go to "my space" → choose formula
2. Click "add to cart" (ajouter au panier)
3. In cart: pay online OR select "pay later" for in-studio payment
4. Click "confirm payment" (confirmer le paiement)
5. Check email (including spam) for confirmation

**Booking a Class:**
1. Login to bsport
2. Calendar view shows available sessions
3. Click "reserve" (réserver) on desired session
4. If no active pass: bsport prompts to choose/purchase one
5. Can pay on-site or online
6. Email confirmation sent

**Booking Multiple Classes:**
- Instead of "reserve a session" click "add sessions" (ajouter des séances)
- Select multiple dates from the right panel
- Shows in green if already registered
- Can book multiple sessions at once for same time slot
- **Note:** Can be slow — recommend using WiFi and computer

**Canceling a Class:**
1. Go to profile → "history" (historique)
2. Find the session
3. Click cancel → confirm
4. Email confirmation sent
5. Can verify in "history" if cancellation worked

**Registering for Workshop/Retreat:**
1. Login to bsport or go via studio website
2. Select workshop → add to cart
3. Choose payment: online or "pay later"

**Subscribing to Membership:**
1. Login → go to "Subscriptions" (Abonnements) top right
2. Choose available subscription
3. Follow guided flow

---

## Studio Backoffice (Staff Interface) — Adam to Map

The backoffice is where studio staff manage everything. Based on member portal structure, the staff side likely contains:

### Expected Staff Sections

| Section | Purpose | What to Test |
|---------|---------|-------------|
| **Dashboard/Home** | Overview, stats, alerts | What's on landing page? |
| **Calendar** | Create/edit classes, manage schedule | How to create recurring class? |
| **Bookings** | View all bookings, manage cancellations | Where's the full booking list? |
| **Members** | Member database, profiles, search | How to find a member? Edit profile? |
| **Passes/Products** | Create passes, set pricing | How to create new pass type? |
| **Memberships** | Subscription management, renewals | Where are active memberships listed? |
| **Payments** | Transactions, refunds, payouts | Where's the payment history? |
| **Marketing** | Email campaigns, automations | Where are email templates? |
| **Reports** | Analytics, attendance, revenue | What reports are available? |
| **Settings** | Studio info, integrations, access control | How to connect Kisi? |
| **Staff/Users** | Team management, permissions | Can you add staff accounts? |

---

## API Access

**No official public API documentation found.**

However, developers have reverse-engineered it:
- Go to backoffice.bsport.io
- Open browser DevTools → Network tab
- Extract token from Authorization headers
- Extract member ID from query strings

### Discovered API Endpoint (from GitHub: angristan/bsport-charts)

**Base URL:** `https://api.production.bsport.io/api/v1/`

**Authentication:** Token-based via header
```
Authorization: Token <your-token>
```

**Booking Endpoint:**
```
GET https://api.production.bsport.io/api/v1/booking/?page=1&page_size=50&mine=true&member=<member_id>
```

**Headers required:**
- `Accept: application/json`
- `Authorization: Token <token>`

**Response fields observed:**
- `id` — Booking ID
- `name` — Class name
- `date` — Session datetime
- `attendance` — Boolean (attended?)
- `booking_status_code` — Status code
- `consumer` — Consumer ID
- `offer` — Offer/Class ID
- `member` — Member ID
- `establishment` — Studio location ID
- `coach` — Instructor ID
- `level` — Level ID
- `meta_activity` — Activity type ID
- `credit_consumed` — Credits used
- `was_refunded` — Refund status
- `is_discardable` — Can be cancelled?
- `offer_duration_minute` — Session length
- `recurrence_rule_booking` — Recurring session info
- `date_canceled` — Cancellation date (null if active)
- `spot_id` — Reserved spot number

**Pagination:** Uses `page` and `page_size` query params. Response includes `links.next` for next page.

**GitHub tool:** `angristan/bsport-charts` — generates booking visualizations from this API

---

## Known Integrations

| Integration | Purpose | Status |
|-------------|---------|--------|
| Kisi | Access control / door entry | Active |
| Stripe | Payment processing | Active (with additional bsport fees) |
| PayPal | Alternative payment | Reports of issues |
| ClassPass | Marketplace | Not confirmed |

---

## Common Issues (from reviews — Adam to verify current status)

1. **Double charging** — Some memberships charged twice
2. **Missing schedule** — Classes not appearing for clients
3. **Email list mishandling** — Unsubscribed clients still receiving emails
4. **Payout delays** — Funds transfer stopped without notice (reported Sep 2025)
5. **Feature limitations** — Cannot assign two teachers per course
6. **Support availability** — Only weekdays 8AM-5PM

---

## Adam's Exploration Log

> **Adam:** Fill this in as you click. What did you find? What worked? What confused you?

### Section: ________________
**Date/Time:** ________________
**What I clicked:** ________________
**What happened:** ________________
**Confusing?:** Yes / No
**Questions for Miha:** ________________

---

## Test Tasks (for when Adam claims supremacy)

1. Create a new class in the schedule
2. Book a member into a class
3. Cancel a booking
4. Check a member's membership status
5. Create a membership pass
6. Find the marketing/email section
7. Pull a booking report
8. Configure access control settings

---

## Questions for bsport Support / Account Manager

- Is there official API documentation?
- How do we export member data?
- Can we customize the mobile app further?
- What's the timeline for multi-teacher assignment?
- How do payout schedules work?

---

## Miha's Research Notes

### Search results summary:
- **Yogama tutorial (French studio):** Shows member-facing features — account creation, cart checkout, booking, subscription management. Best hands-on guide found.
- **bsport-charts (GitHub):** Confirms API is token-based, accessible via browser inspection
- **Kisi docs:** bsport has access control integration with door entry
- **Trustpilot:** Mixed reviews (3.7-3.9/5). Praise for support team responsiveness, complaints about billing/contract terms
- **Bobclass comparison:** bsport is modular, complex, annual contract, requires dedicated manager

### Documentation gaps identified:
- **No public API docs** — only reverse-engineered tools on GitHub
- **No comprehensive feature guide** found online
- **No official help center** accessible without login
- Most "documentation" is competitor comparisons or reverse-engineered GitHub projects
- French tutorial (yogama.fr) is the best member-facing guide found
- Staff backoffice documentation is virtually non-existent publicly

### bsport from Competitor/Industry Perspective
- "Next generation all-inclusive management platform"
- "Fully streamlined with everything you need to run your studio"
- "Automated marketing suite" for customer acquisition/retention
- "Simple and seamless payment process"
- Standard OR fully branded customer experiences
- Target: Pilates, Yoga, Crossfit, Fitness, Dance, Wellness

### bsport Features (from Kisi / Industry Review)
- **Booking management:** Intuitive for both staff and clients
- **Webshop:** Sell products online
- **Video-on-demand (VOD):** Virtual class offerings
- **Marketplace integrations:** ClassPass, Urban Sports Club, etc.
- **Access control:** Kisi integration for door entry
- **Automated marketing suite:** Email campaigns, retention tools
- **Multi-location support:** Centralized management for franchises
- **Data insights:** Business analytics and reporting
- **Custom branded apps:** White-label iOS/Android apps
- **Zoom integration:** Virtual classes
- **Payroll:** Staff payment management (with known limitation: 1 teacher per class)
- **Check-in:** Member attendance tracking
- **Billing:** Integrated payment processing

---

## Resources

- **Member tutorial (French):** https://www.yogama.fr/tutoriels-bsport/
- **GitHub API tool:** https://github.com/angristan/bsport-charts
- **Kisi integration docs:** https://docs.kisi.io/marketplace/fitness/bsport
- **Trustpilot reviews:** https://www.trustpilot.com/review/bsport.io
- **bsport login:** https://backoffice.bsport.io/login

---

## Adam's Hands-On Findings (2026-05-15)

**bsport Status: FULLY MAPPED**

### The Numbers
- **246 members**
- **55 weekly bookings, 45 confirmed, 10 cancelled**
- **Class fill rates: 20-35%** — massive growth potential
- **227 invoices, ALL paid (0.00€ due)** — excellent cash flow
- **10-class packs expiring Aug 2025** — 9 members to re-engage

### Critical UX Gap Found
**NO "Add attendee" button exists in backoffice.** Adam tried 7+ paths. Staff cannot manually add walk-ins or comp guests to classes directly. Only "Add a recurring booking" exists (auto-enrolls into recurring classes). This is a platform limitation, not a navigation issue.

### The Solution (Help Center Article 4210921)

**How to manually add a member to a single class:**
1. Calendar or Schedule tab
2. Select the session
3. Click "Manage my bookings"
4. Search for the member in the search bar
5. Click "Book In"
6. Select a valid pass the member has, or bill a new one using "Bill a new pass" tab

**Alternative: Create member + book in one step**
1. Calendar → Session → Manage my bookings
2. Click the **+** icon (top right, available on ALL pages)
3. Fill form (First Name, Last Name, Email required)
4. Click "Save" → creates member AND books them into the session

**For walk-ins / comp guests:**
1. First enable: Settings → Customize → Check "Allow guest booking"
2. Make passes compatible: Products → Passes → Edit → Check "Compatible with guest booking"
3. Make sessions compatible: Calendar → Session → Edit → Check "Allow guest booking"
4. Then book: Calendar → Session → Manage bookings → Book as guest
5. A guest member record is auto-created with a "guest" icon

### Pricing (matches heatlagos.com)
- Intro: 79€ | Summer: 390€ | 12-Mo: 125€/mo | 1-Mo: 160€
- Yearly: 1,200€ | 10-Pack: 180€ | Vacation: 59€ | Drop-in: 22€

### Marketing Section Note
bsport backoffice is a Single Page Application (React/Vue). Headless tools only see the empty shell before JS renders. The Marketing section DOES work in Chrome with JavaScript enabled.

**Marketing includes:**
- Email campaigns & templates
- Smartlists (segmented member lists)
- Automated communication flows
- Pre-launch signups
- Newsletter management

**No activation needed** — just use Chrome, not headless scraping.

### Known UX Issues (Confirmed)
- Teacher swap is 4 clicks deep with no quick button
- No "Add attendee" direct button — must use Calendar → Manage bookings path
- Support only weekdays 8AM-5PM

---

*Last updated: 2026-05-16 by Miha — Adam's exploration COMPLETE. Manual roster path documented. Standing by for next task.*
