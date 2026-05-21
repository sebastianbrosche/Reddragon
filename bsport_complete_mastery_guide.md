# BSPORT COMPLETE MASTERY GUIDE
## For Heat Lagos Operations | Compiled by Miha
### Source: bsport Help Center (intercom.help/bsport-helpcenter/en/)
### Last Updated: 2026-05-15

---

## TABLE OF CONTENTS

1. [Quick Answers to Adam's Questions](#quick-answers)
2. [Calendar & Scheduling](#calendar)
3. [Members & CRM](#members)
4. [Passes & Products](#products)
5. [Marketing & Communications](#marketing)
6. [Transactions & Billing](#transactions)
7. [Dashboard & Reporting](#dashboard)
8. [Settings & Configuration](#settings)
9. [Full Article Index](#index)

---

## QUICK ANSWERS TO ADAM'S QUESTIONS

### ❓ "How do I manually add a member to a class roster?"

**ANSWER: There are 3 ways to do this:**

**Method 1: From Calendar/Schedule (Recommended)**
1. Go to **Calendar** or **Schedule** tab
2. Select the session you want
3. Click **"Manage bookings"**
4. Search for the member in the search bar
5. Click **"Book In"**
6. Select a valid pass the member has, or bill a new one using "Bill a new pass" tab
7. Done!

**Method 2: Add Member + Book in One Step**
1. Go to **Calendar** > Select session > **"Manage my bookings"**
2. Click the **+ icon** (top right, available on all pages)
3. Fill in the form (First Name, Last Name, Email required)
4. Click **"Save"** — this creates the member AND books them into the session

**Method 3: Book a Guest (walk-ins, comp guests)**
1. First, enable guest booking: **Settings** > **Customize** > Check **"Allow guest booking"**
2. Optionally set limits: Settings > Personalization > "Allow booking for a guest" > Set limit per week/month/year
3. Make passes compatible: **Products** > **Passes** > Edit pass > Check "Compatible with booking for a guest"
4. Make sessions compatible: **Calendar** > Select session > **Edit** > Check "Allow booking for a guest"
5. Then book: Calendar > Session > Manage bookings > Book as guest

> **IMPORTANT:** When managing from Calendar, a guest member record is automatically created with a "guest" icon. The relationship between member and guest is also created automatically.

---

### ❓ "How do I swap a substitute teacher?"

**ANSWER: 4 clicks, plus propagation to multiple sessions**

**For a single session:**
1. Go to **Calendar**
2. Select the session
3. Click **"Edit"**
4. In the teacher section, select substitute from dropdown
5. Click **Save**

**For multiple sessions (teacher absent for a week):**
1. Calendar > Select FIRST session > **Edit**
2. Select substitute teacher in the dropdown
3. Check **"Apply this modification to the following sessions"**
4. A list appears — check off the sessions affected
5. If another substitute was already set for some sessions, choose which to keep
6. Click **Save**

> **Adam's finding confirmed:** This IS buried 4 clicks deep. No quick swap button exists.

---

### ❓ "How do I extend a 10-class pack that's expiring in August?"

**ANSWER: Extend validity from member profile**
1. Search for the member in the search bar
2. Click on their **'Pass'** tab
3. Click on the pass to extend
4. Click **'Extend validity'**
5. Choose: number of additional days OR new expiry date
6. Add a note if needed (e.g., "Summer extension — 30 extra days")
7. Click **"Create"**
8. You can cancel the extension later by clicking the bin icon

> **Pro tip:** Do this BEFORE the pass expires. Once expired, members lose access and you have to create a new pass or reactivate the old one.

---

### ❓ "The Marketing page is empty in my browser — what's wrong?"

**ANSWER: React/Vue SPA rendering issue**

bsport backoffice is a **Single Page Application (SPA)**. Many pages load content dynamically via JavaScript AFTER the initial page render. Headless/scraping tools only see the initial empty shell.

**Solution:** Use a **real Chrome browser with JavaScript enabled** (which Adam is doing). The Marketing section should work fine in Chrome.

**Marketing section includes:**
- Email campaigns
- Smartlists (segmented member lists)
- Newsletter templates
- Automated communication flows
- Pre-launch signups

> **Note:** Adam confirmed Marketing page is empty in accessibility tree. This is expected for SPAs. Use Chrome for full access.

---

## CALENDAR & SCHEDULING

### Create, Edit, Cancel or Delete Sessions

**Creating a session — 2 ways:**

**Way 1: From Calendar**
1. Click **'Add Sessions'**
2. Select the activity
3. Fill the form:
   - Name/description (can set custom name for special events)
   - Date, time, duration
   - Number of students (capacity)
   - Waiting list size
   - Teacher
4. Choose: single session OR recurring (monthly/weekly/daily)
5. Click **'Save'**

**Way 2: From My Studio**
1. **My Studio** > **Group Activities**
2. Select activity
3. Click **'Add sessions'**
4. Same form as above

**Modifying a session:**
1. Calendar > Click **"Edit"** on the session
2. Modify: activity, name, description, date, time, duration, capacity, waiting list, teacher
3. Change teacher OR select substitute
4. Choose: modify single session OR similar sessions
5. Click **Save**

> **WARNING:** Modifying only affects FUTURE sessions, not past ones.

**Cancel a session:**
1. Calendar > Select session > Click **Cancel**
2. A window appears — notify clients, cancel similar sessions
3. **WARNING:** Reservations and waiting list are NOT restored automatically

**Restore a cancelled session:**
1. Calendar > Click cancelled session
2. Click **'Restore session'**
3. **WARNING:** Bookings and waiting list are NOT restored — you must manually re-register students

**Delete a session:**
1. Must cancel it first
2. Calendar > Click session
3. Click **Delete**
4. **WARNING:** Cannot delete a session with reservations

---

### Call the Roll (Attendance Tracking)

**When enabled, you can mark members as Present/Absent.**

1. Go to **Calendar**
2. If roll call is activated, you'll see red/green icons indicating which sessions need validation
3. Click the icon to make the roll call
4. Toggle **Present/Absent** for each member
5. Click **"Validate"**
6. You can still modify after validation for a short period

**Bulk validation:**
- Use **"Validate all calls"** button on Calendar page to validate multiple sessions at once

**Related feature:** No-show penalties can be configured (see Settings)

---

### Recurring Sessions

**Create recurring sessions:**
1. Calendar > Add Sessions
2. In the form, select recurrence: weekly/monthly/daily
3. Set end date or number of occurrences
4. Save

**Create recurring session over multiple days:**
1. Calendar > Add Sessions
2. Set recurrence pattern
3. Select multiple days of the week
4. Save

**Book on recurring basis through session:**
1. Calendar > Select session
2. Manage bookings
3. Book member with recurring option
4. Member gets enrolled in all future instances

---

### Session Management Tips

**Hide cancelled sessions from clients:**
- Manager side: Calendar > Wheel icon > **'Hide cancellations'**
- Client side: Settings > Personalization > Uncheck 'Show cancelled sessions'

**Add notes to a session:**
1. Calendar > Select session
2. Add notes (visible to staff, not clients)

**Postpone a session:**
1. Calendar > Select session
2. Edit
3. Change the date
4. Save + notify clients

**Custom booking window:**
- Settings > Personalization > Set how far in advance members can book

---

## MEMBERS & CRM

### Create a Member

**Method 1: Add new member (standalone)**
1. Click **+ icon** (top right, available on ALL pages)
2. Fill form: First Name, Last Name, Email (required)
3. Click **"Save"**

**Method 2: Add member when managing a session**
1. Calendar/Schedule > Select session > **"Manage my bookings"**
2. Click **+ icon**
3. Fill form + member is automatically booked into the session

---

### Managing a Member Profile

**Access a member profile — 2 ways:**

**Way 1:** Members section > Search > Click **"View"**
**Way 2:** Search bar (top right of any page) > Type name > Click result

**Profile has 12 tabs:**
1. **General** — Basic info, tags, communication preferences, notes
2. **Bookings** — All reservations, present/absent status
3. **Passes** — Active passes, credits, validity
4. **Subscriptions** — Memberships, auto-renewal status
5. **Billing** — Invoices, payments, refunds
6. **Credit** — Internal account balance
7. **Documents** — Uploaded files (waivers, medical forms)
8. **Tasks/Notifications** — Staff reminders about this member
9. **Relationships** — Family accounts, guest relationships
10. **Communication** — Email history
11. **Statistics** — Attendance, spending, activity
12. **Settings** — Password, login email

---

### Member Actions

**Add notes to a member:**
1. Member profile > General tab
2. Click **"Add note"**
3. Write medical info, personal notes, follow-up reminders
4. Save

**Add tags (CRM segmentation):**
1. Member profile > General tab
2. **"My Tags"** section
3. Create categories and subcategories
4. Example: Category "Main Sport" > Subcategories: Fitness, Yoga, Cross-Fit
5. Apply tags to filter and segment members

**Merge duplicate accounts:**
1. Member profile > General tab
2. Click **"Merge"**
3. Search for similar account
4. Use arrows to choose which account to keep (right one gets deleted)
5. Click **Save**

**Archive a member:**
1. Member profile
2. Click **"Archive"**
3. Member becomes inactive but data is preserved

**Change member email:**
1. Member profile > Edit
2. Update email field
3. Save

---

### Bookings Management

**Register member for a course:**
1. Member profile > **Bookings** tab
2. Click **"Subscribe"**
3. Select subscription/pass
4. Fill details
5. Click **"Check"** to proceed to payment

**Make a member absent:**
1. Member profile > Bookings tab
2. Find the booking
3. Click **"Present"** → toggles to **"Absent"**

**Cancel a member's reservation:**
1. Member profile > Bookings tab
2. Click **X** (cross symbol)
3. Confirm
4. Member is automatically re-credited

**Schedule recurrent booking through member profile:**
1. Member profile > Bookings tab
2. Click **"Schedule recurrent booking"**
3. Select sessions
4. Member gets enrolled in all instances

---

### Billing Actions

**Invoice a member:**
1. Member profile > **Billing** tab
2. Click **"Invoice"**
3. Add products/subscriptions to cart
4. Apply discounts if needed
5. Click **"€ Payment"**
6. Choose payment method
7. Enter amount
8. Click **"Payment"**
9. Click **"Save"**
10. Confirm invoice date (for delayed payments)

**Refund a member:**
1. Member profile > Billing tab
2. Find the invoice
3. Click refund option
4. Choose: full refund or partial refund
5. Can refund to credit (internal account) or original payment method

**Credit a client's account (without payment):**
1. Member profile > Credit tab
2. Add credit amount
3. Use credit for future purchases

**Extend pass validity:**
(See Quick Answers section above)

---

## PASSES & PRODUCTS

### Pass Management

**Create a pass:**
1. **Products** > **Passes**
2. Click **"Create pass"**
3. Fill form:
   - Name, description
   - Number of credits
   - Validity period
   - Price
   - Compatible activities
   - "Compatible with guest booking" (yes/no)
   - Online purchase availability
4. Save

**Edit a pass:**
1. Products > Passes
2. Click pen icon on the pass
3. Modify settings
4. Save

**Check pass compatibility with activities:**
1. Products > Passes
2. Edit pass
3. Select which activities/workshops the pass is valid for
4. Save

> **Important:** If a pass is not compatible with a session, it won't appear as an option when booking.

---

### Memberships / Subscriptions

**Create a subscription:**
1. **Products** > **Subscriptions**
2. Click **"Create subscription"**
3. Fill form:
   - Name, description
   - Billing frequency (monthly, yearly)
   - Price
   - Commitment period
   - Cancellation terms
4. Save

**Subscribe a member:**
1. Member profile > Bookings tab
2. Click **"Subscribe"**
3. Select subscription
4. Set number of months
5. Set first billing date
6. Apply special offers (free months, discounts)
7. Click **"Check"** → proceed to payment

**Cancel a subscription:**
1. Member profile > Subscriptions tab
2. Select subscription
3. Click **"Cancel"**
4. Choose: immediate or end of period

**Pause a subscription:**
1. Member profile > Subscriptions tab
2. Select subscription
3. Click **"Pause"**
4. Set pause duration

**Deactivate auto-renewal:**
1. Member profile > Subscriptions tab
2. Select subscription
3. Toggle auto-renewal off

---

## MARKETING & COMMUNICATIONS

### Email Campaigns

**Send a message to students (from Calendar):**
1. Calendar > Select session
2. Click **"Send a message"**
3. Choose recipients: all booked members, waiting list, or specific individuals
4. Write message
5. Send

**Send a direct message to a member:**
1. Member profile
2. Click **"Send message"**
3. Write and send

**Create email templates:**
1. **Marketing** > **Email templates**
2. Click **"Create template"**
3. Design email (use bsport editor)
4. Save

**Send newsletter to all customers:**
1. Marketing > Newsletters
2. Select template or create new
3. Choose audience (all members, or filtered by tags)
4. Schedule or send immediately

---

### Smartlists (Segmentation)

**Create a Smartlist:**
1. **Marketing** > **Smartlists**
2. Click **"Add a Smartlist"**
3. Add filters:
   - Member information (tags, registration date, etc.)
   - Booking history (attended X sessions, last visit, etc.)
   - Pass status (active, expired, about to expire)
   - Subscription status
4. Click **"Add"**
5. Save Smartlist

**Use Smartlists:**
- Send targeted emails to specific segments
- Export member lists
- Track engagement

**Example Smartlists for Heat Lagos:**
- "10-class pack holders expiring in August"
- "Members who haven't visited in 30 days"
- "Heat Pilates regulars (5+ visits)"
- "New members (joined last 30 days)"

---

### Automated Communication Flows

**Set up automated emails:**
1. Marketing > Automation
2. Create flow:
   - Trigger: new member, class reminder, pass expiring, no-show, etc.
   - Delay: immediate, X hours before, X days after
   - Action: send email, add tag, create task
3. Save and activate

**Pre-launch signups:**
1. Marketing > Pre-launch
2. Create signup form for new classes/workshops
3. Share link with members
4. Track interest before launch

---

## TRANSACTIONS & BILLING

### Process a Refund

**Full refund:**
1. Find the invoice (member profile > Billing, or Transactions > Invoices)
2. Click **"Refund"**
3. Choose: refund to original payment method OR credit to internal account
4. Confirm

**Partial refund:**
1. Same as above
2. Enter partial amount
3. Confirm

**Refund without cancelling transaction (credit):**
1. Invoice > Click specific refund option
2. Amount is credited to member's internal account
3. Member can use credit for future purchases

---

### Manage Invoices

**Cancel an invoice:**
1. Find invoice
2. Click **"Cancel Invoice"**
3. Invoice marked as cancelled
4. Associated products are deleted

**Download invoice PDF:**
1. Invoice > Click paper clip icon
2. Download and print

**Record a manual payment:**
1. Unpaid invoice
2. Click **"Record payment"**
3. Select payment method
4. Enter amount
5. Confirm

**Process unpaid invoice as paid (manual):**
1. Invoice > Click **"Mark as paid"**
2. Record payment method
3. Confirm

---

### Payment Methods

**Add payment method for member:**
1. Member profile > General tab
2. Add credit card or SEPA
3. Save

**Delete payment method:**
1. Member profile
2. Find payment method
3. Click delete

**Change payment method for subscription:**
1. Member profile > Subscriptions
2. Select subscription
3. Click **"Change payment method"**
4. Select new method
5. Save

---

## DASHBOARD & REPORTING

### Dashboard Overview

**What you see:**
- Today's sessions
- Recent bookings
- Revenue summary
- Member activity
- Low-fill alerts (if configured)

**Customize dashboard:**
1. Dashboard > Settings
2. Choose widgets to display
3. Arrange layout
4. Save

---

### Reports

**Available reports:**
1. **Revenue** — daily, weekly, monthly revenue
2. **Attendance** — session attendance rates
3. **Members** — new members, churn, retention
4. **Passes** — pass sales, usage, expirations
5. **Subscriptions** — active, cancelled, paused
6. **Instructors** — classes taught, payroll

**Export reports:**
1. Select report
2. Set date range
3. Click **"Export"**
4. Download CSV/Excel

---

## SETTINGS & CONFIGURATION

### Personalization

**Customize member calendar:**
1. **Settings** > **Personalization**
2. Options:
   - Show/hide cancelled sessions
   - First day of week (Sunday/Monday)
   - Booking window (how far in advance)
   - Cancellation deadline
   - Guest booking settings
3. Save

**Customize notifications:**
1. Settings > Notifications
2. Set what members receive:
   - Booking confirmations
   - Reminders (24h before, 1h before)
   - Cancellation notices
   - Waitlist notifications
   - Pass expiration warnings
3. Save

---

### Studio Settings

**Studio information:**
1. **My Studio** > **Settings**
2. Update: name, address, contact info, logo, colors
3. Save

**Group activities:**
1. My Studio > Group Activities
2. Create/edit activities (Pilates, Yoga, Sculpt, etc.)
3. Set default duration, capacity, description
4. Save

**Teachers/Instructors:**
1. My Studio > Teachers
2. Add teacher profiles
3. Set availability
4. Assign to activities

---

## FULL ARTICLE INDEX

### Calendar (39 articles)
| Article | URL |
|---------|-----|
| Book a session for a family member/a friend | https://intercom.help/bsport-helpcenter/en/articles/5335445 |
| View lessons as teacher on mobile app | https://intercom.help/bsport-helpcenter/en/articles/5331994 |
| Display order of sessions in calendar | https://intercom.help/bsport-helpcenter/en/articles/6474912 |
| Call the roll | https://intercom.help/bsport-helpcenter/en/articles/7263031 |
| Launch Zoom meeting from bsport | https://intercom.help/bsport-helpcenter/en/articles/5591326 |
| Download summary of bookings for the day | https://intercom.help/bsport-helpcenter/en/articles/5373298 |
| Restore cancelled session and re-register | https://intercom.help/bsport-helpcenter/en/articles/5384850 |
| Manage online sessions | https://intercom.help/bsport-helpcenter/en/articles/3830979 |
| Apply substitute teacher over several sessions | https://intercom.help/bsport-helpcenter/en/articles/6912376 |
| Create, edit, cancel or delete sessions | https://intercom.help/bsport-helpcenter/en/articles/3271716 |
| Book a member into a class | https://intercom.help/bsport-helpcenter/en/articles/4210921 |
| Create task or notification | https://intercom.help/bsport-helpcenter/en/articles/3650861 |
| Register members for all sessions of group activity | https://intercom.help/bsport-helpcenter/en/articles/5988793 |
| Book on recurring basis through session | https://intercom.help/bsport-helpcenter/en/articles/4293420 |
| Add different levels to sessions | https://intercom.help/bsport-helpcenter/en/articles/6197507 |
| Show sessions only for some members | https://intercom.help/bsport-helpcenter/en/articles/6154328 |
| View activities and workshops | https://intercom.help/bsport-helpcenter/en/articles/4126352 |
| Create hybrid session | https://intercom.help/bsport-helpcenter/en/articles/7969371 |
| Add tags to sessions | https://intercom.help/bsport-helpcenter/en/articles/6149203 |
| Send message to students | https://intercom.help/bsport-helpcenter/en/articles/3362225 |
| Create invisible session | https://intercom.help/bsport-helpcenter/en/articles/6001216 |
| Create recurring session over several days | https://intercom.help/bsport-helpcenter/en/articles/5013015 |
| Postpone session by changing date | https://intercom.help/bsport-helpcenter/en/articles/4318391 |
| Bulk cancel, grouped cancellation | https://intercom.help/bsport-helpcenter/en/articles/4396433 |
| Mass cancellation of sessions | https://intercom.help/bsport-helpcenter/en/articles/4236903 |
| Create session using spot scheduling | https://intercom.help/bsport-helpcenter/en/articles/5397536 |
| Send Zoom link manually | https://intercom.help/bsport-helpcenter/en/articles/6014423 |
| Time Clock tool | https://intercom.help/bsport-helpcenter/en/articles/6132256 |
| Personalize calendar | https://intercom.help/bsport-helpcenter/en/articles/8170552 |
| Bulk selection in waiting list | https://intercom.help/bsport-helpcenter/en/articles/8523226 |
| Push sessions to marketplace | https://intercom.help/bsport-helpcenter/en/articles/8712119 |
| Add notes to session | https://intercom.help/bsport-helpcenter/en/articles/8825371 |
| Sunday as first day | https://intercom.help/bsport-helpcenter/en/articles/8975054 |
| Check why members can't see session | https://intercom.help/bsport-helpcenter/en/articles/8979136 |
| Remove cancelled session from calendar | https://intercom.help/bsport-helpcenter/en/articles/8985128 |
| Customize booking window | https://intercom.help/bsport-helpcenter/en/articles/11885682 |
| Sync to Apple Calendar | https://intercom.help/bsport-helpcenter/en/articles/12608643 |
| Swap pass on existing booking | https://intercom.help/bsport-helpcenter/en/articles/14195918 |
| Aggregator spot capping | https://intercom.help/bsport-helpcenter/en/articles/15073008 |

### Members (75 articles)
| Article | URL |
|---------|-----|
| Create member's account | https://intercom.help/bsport-helpcenter/en/articles/3285692 |
| Managing a member | https://intercom.help/bsport-helpcenter/en/articles/3286228 |
| Add notes for students | https://intercom.help/bsport-helpcenter/en/articles/3329345 |
| Archive a member | https://intercom.help/bsport-helpcenter/en/articles/5790088 |
| Create member account (detailed) | https://intercom.help/bsport-helpcenter/en/articles/3285692 |
| Add document for member | https://intercom.help/bsport-helpcenter/en/articles/3527955 |
| Add payment method | https://intercom.help/bsport-helpcenter/en/articles/6193562 |
| Edit member password | https://intercom.help/bsport-helpcenter/en/articles/7973153 |
| Adjust client balance | https://intercom.help/bsport-helpcenter/en/articles/5870925 |
| Merge duplicated accounts | https://intercom.help/bsport-helpcenter/en/articles/4211090 |
| Unsubscribe from communications | https://intercom.help/bsport-helpcenter/en/articles/3850740 |
| Regularize student deposit | https://intercom.help/bsport-helpcenter/en/articles/3307109 |
| Create subscription after 1st reservation | https://intercom.help/bsport-helpcenter/en/articles/3326321 |
| Cashout customer internal account | https://intercom.help/bsport-helpcenter/en/articles/4198204 |
| Search members from phone | https://intercom.help/bsport-helpcenter/en/articles/5495766 |
| Change member email | https://intercom.help/bsport-helpcenter/en/articles/8866046 |
| Schedule recurrent booking through profile | https://intercom.help/bsport-helpcenter/en/articles/4473496 |
| Book for a guest (manager) | https://intercom.help/bsport-helpcenter/en/articles/6175130 |
| Recurring booking for private appointments | https://intercom.help/bsport-helpcenter/en/articles/4835249 |
| Cancellation management | https://intercom.help/bsport-helpcenter/en/articles/3826454 |
| Reservation without charging credit | https://intercom.help/bsport-helpcenter/en/articles/3619141 |
| Cancel recurrent booking | https://intercom.help/bsport-helpcenter/en/articles/5454249 |
| Check why member can't register | https://intercom.help/bsport-helpcenter/en/articles/8929733 |
| Extend pass validity | https://intercom.help/bsport-helpcenter/en/articles/4592119 |
| Allocate pass to another account | https://intercom.help/bsport-helpcenter/en/articles/5563502 |
| Subscriptions start in past | https://intercom.help/bsport-helpcenter/en/articles/6573753 |
| Deactivate auto-renewal | https://intercom.help/bsport-helpcenter/en/articles/5373622 |
| Send direct payment link | https://intercom.help/bsport-helpcenter/en/articles/5621567 |
| Refund receipt after balance adjustment | https://intercom.help/bsport-helpcenter/en/articles/5554174 |
| Allow balance for purchases | https://intercom.help/bsport-helpcenter/en/articles/5948782 |
| Billing a student | https://intercom.help/bsport-helpcenter/en/articles/4726929 |
| Bill product from shop | https://intercom.help/bsport-helpcenter/en/articles/5326909 |
| Cash in scheduled payment | https://intercom.help/bsport-helpcenter/en/articles/6193502 |
| Disable auto-payment of subscription | https://intercom.help/bsport-helpcenter/en/articles/5546433 |
| Personalized footer on invoices | https://intercom.help/bsport-helpcenter/en/articles/5258360 |
| Get invoice PDF | https://intercom.help/bsport-helpcenter/en/articles/3525096 |
| Refund paid invoice (credit) | https://intercom.help/bsport-helpcenter/en/articles/4417893 |
| Change payment method for subscription | https://intercom.help/bsport-helpcenter/en/articles/4197689 |
| Cancel invoice | https://intercom.help/bsport-helpcenter/en/articles/3968196 |
| Refund after online payment | https://intercom.help/bsport-helpcenter/en/articles/3796424 |
| Restart membership + payment | https://intercom.help/bsport-helpcenter/en/articles/5187521 |
| Edit product of subscription | https://intercom.help/bsport-helpcenter/en/articles/5580055 |
| Credit account without payment | https://intercom.help/bsport-helpcenter/en/articles/4135913 |
| Use credit balance for purchase | https://intercom.help/bsport-helpcenter/en/articles/4126048 |
| Non-recurring subscription | https://intercom.help/bsport-helpcenter/en/articles/4108220 |
| Down payment after cash inflow | https://intercom.help/bsport-helpcenter/en/articles/4305169 |
| Bill member for free | https://intercom.help/bsport-helpcenter/en/articles/4301456 |
| Disputed charge | https://intercom.help/bsport-helpcenter/en/articles/5537842 |
| Payments in future | https://intercom.help/bsport-helpcenter/en/articles/3324668 |
| Payment by credit card | https://intercom.help/bsport-helpcenter/en/articles/3447782 |
| Process unpaid as paid (manual) | https://intercom.help/bsport-helpcenter/en/articles/4258263 |
| Schedule closure of subscription | https://intercom.help/bsport-helpcenter/en/articles/4569850 |
| Send direct message to member | https://intercom.help/bsport-helpcenter/en/articles/14686371 |
| Relationship accounts | https://intercom.help/bsport-helpcenter/en/articles/5948514 |
| Sharing passes among members | https://intercom.help/bsport-helpcenter/en/articles/3361756 |
| Managing child's account | https://intercom.help/bsport-helpcenter/en/articles/4406625 |
| Share appointment pass | https://intercom.help/bsport-helpcenter/en/articles/4764653 |
| Restore cancelled appointment | https://intercom.help/bsport-helpcenter/en/articles/4621619 |
| Giftcard (member side) | https://intercom.help/bsport-helpcenter/en/articles/5900452 |
| Charge gift card | https://intercom.help/bsport-helpcenter/en/articles/5783348 |
| Change login email | https://intercom.help/bsport-helpcenter/en/articles/5864332 |
| Add new email address | https://intercom.help/bsport-helpcenter/en/articles/6413869 |
| Understand member baskets | https://intercom.help/bsport-helpcenter/en/articles/6059046 |
| Decline codes | https://intercom.help/bsport-helpcenter/en/articles/5657252 |
| Multi-location invoice link | https://intercom.help/bsport-helpcenter/en/articles/5592364 |

### Products (80 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868488-products

### Marketing (85 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868518-marketing

### My Studio (56 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868469-my-studio

### Transactions (31 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868505-transactions

### Settings (133 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868535-settings

### Reporting (28 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/3868534-reporting

### FAQ - Members (29 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/2348822-faq-members

### FAQ - General (10 articles)
**Collection URL:** https://intercom.help/bsport-helpcenter/en/collections/2348836-frequently-asked-questions

---

## ADAM'S QUICK REFERENCE CARD

**Login:** https://backoffice.bsport.io/
**Email:** adambot@yogaforbjj.net
**Password:** kimiclaw321

### Daily Tasks

**Check today's classes:**
Dashboard → Today's sessions

**Add walk-in member to class:**
Calendar → Session → Manage bookings → + icon → Fill form → Save

**Mark attendance:**
Calendar → Session → Roll call icon → Present/Absent → Validate

**Swap teacher (sick day):**
Calendar → Session → Edit → Teacher dropdown → Select substitute → Save → Apply to future sessions if needed

**Extend expiring pass:**
Search member → Pass tab → Click pass → Extend validity → Add days → Create

**Send message to class:**
Calendar → Session → Send message → Write → Send

### Weekly Tasks

**Check low-fill classes:**
Calendar → Look for sessions with <50% bookings

**Review expiring passes:**
Members → Filter by pass expiration → Extend or re-engage

**Run reports:**
Reporting → Revenue / Attendance / Members

**Create Smartlist for re-engagement:**
Marketing → Smartlists → Filter: last visit >30 days → Save

### Emergency Procedures

**Teacher calls in sick:**
1. Calendar → Session → Edit
2. Substitute teacher dropdown
3. If absent for multiple days: check "Apply to following sessions"
4. Notify members: Calendar → Session → Send message

**Member wants to cancel:**
1. Member profile → Bookings tab
2. Find booking → Click X
3. Member auto-credited

**System issue / Can't access:**
1. Check: Settings > Personalization (browser compatibility)
2. Use Chrome with JavaScript enabled
3. Contact support: in-app chat (weekdays 8AM-5PM)
4. German support available

---

## KNOWN UX ISSUES (Adam's Findings + Help Center Confirmation)

| Issue | Status | Workaround |
|-------|--------|------------|
| No direct "Add attendee" button | Confirmed | Use Calendar → Manage bookings → Book In |
| Teacher swap buried 4 clicks deep | Confirmed | Calendar → Edit → Teacher dropdown |
| Marketing page empty in headless mode | Confirmed | Use Chrome with JS enabled |
| No bulk credit adjustment | Confirmed | Must click individually per member |
| Inconsistent navigation | Confirmed | Some sidebar items are links, some buttons |
| No-show penalties need setup | Documented | Settings > Personalization > Penalties |
| Pass compatibility check before booking | Documented | Products > Passes > Edit > Compatible activities |

---

## HEAT LAGOS SPECIFIC SETUPS

### Recommended Smartlists
1. **"August Expirations"** — Passes expiring in next 30 days
2. **"Low Attendance"** — Members with <3 visits this month
3. **"New Members"** — Joined in last 30 days (onboarding)
4. **"Pilates Regulars"** — 5+ Heat Pilates visits
5. **"Recovery Fans"** — Attended Heat Recovery 3+ times

### Recommended Automated Flows
1. **Welcome series** — New member: day 1 (intro), day 3 (class tips), day 7 (feedback)
2. **Re-engagement** — No visit in 14 days → "We miss you" email
3. **Pass expiration** — 7 days before expiry → "Renew now" with discount
4. **Class reminder** — 24h before booking → reminder email
5. **No-show follow-up** — After no-show → "Everything okay?" check-in

### Recommended Pass Setup
- **10-class pack** — €150, 3-month validity, all activities
- **Monthly unlimited** — €180, auto-renew, all activities
- **Intro offer** — 2 weeks unlimited €79 (new members only)
- **Drop-in** — €20 per class
- **Private session** — €80 (1-on-1 with instructor)

---

*Compiled by Miha for Adam [HEAT] | 2026-05-15*
*Source: bsport Help Center — 600+ articles across 15 categories*
*This is a living document. Update as we discover more.*
