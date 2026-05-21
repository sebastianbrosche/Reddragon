import re

with open('/root/.openclaw/workspace/bsport_help_center_clean.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find key sections
sections = re.split(r'\n## ', content)

quick_start = "# bsport QUICK START CHEAT SHEET for Adam\n\n"
quick_start += "> Extracted from the full help center PDF. This covers the essentials to get you moving.\n\n"

# Dashboard section
dashboard = [s for s in sections if s.startswith('Dashboard')]
if dashboard:
    quick_start += "## DASHBOARD — Your Home Base\n\n"
    quick_start += dashboard[0][:3000] + "\n\n"

# Calendar section  
calendar = [s for s in sections if s.startswith('Calendar')]
if calendar:
    quick_start += "## CALENDAR — Creating Classes\n\n"
    # Find key articles about creating activities
    lines = calendar[0].split('\n')
    key_lines = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ['create', 'add', 'schedule', 'activity', 'class', 'booking', 'recurring']):
            key_lines.extend(lines[max(0,i-2):min(len(lines),i+8)])
    quick_start += '\n'.join(key_lines[:3000]) + "\n\n"

# Members section
members = [s for s in sections if s.startswith('Members')]
if members:
    quick_start += "## MEMBERS — Finding People\n\n"
    lines = members[0].split('\n')
    key_lines = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ['find', 'search', 'add', 'create', 'import', 'tag', 'filter']):
            key_lines.extend(lines[max(0,i-2):min(len(lines),i+8)])
    quick_start += '\n'.join(key_lines[:3000]) + "\n\n"

# Products section
products = [s for s in sections if s.startswith('Products')]
if products:
    quick_start += "## PRODUCTS — Passes & Subscriptions\n\n"
    lines = products[0].split('\n')
    key_lines = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ['create', 'pass', 'subscription', 'price', 'credit', 'membership']):
            key_lines.extend(lines[max(0,i-2):min(len(lines),i+8)])
    quick_start += '\n'.join(key_lines[:3000]) + "\n\n"

# Settings section
settings = [s for s in sections if s.startswith('Settings')]
if settings:
    quick_start += "## SETTINGS — Key Configurations\n\n"
    lines = settings[0].split('\n')
    key_lines = []
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in ['integration', 'notification', 'payment', 'stripe', 'access', 'role']):
            key_lines.extend(lines[max(0,i-2):min(len(lines),i+8)])
    quick_start += '\n'.join(key_lines[:3000]) + "\n\n"

quick_start += "\n---\n\n**FULL PDF:** The complete 233-article documentation is in the chat above. Search there for anything not covered here.\n"

with open('/root/.openclaw/workspace/bsport_quick_start.md', 'w', encoding='utf-8') as f:
    f.write(quick_start)

print(f"Quick start created: {len(quick_start)} characters")
