import re

with open('/root/.openclaw/workspace/bsport_help_center_clean.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all articles with their titles and URLs
articles = []
pattern = r'### (.+?)\n\*\*Source:\*\* (https://intercom\.help/bsport-helpcenter/en/articles/(\d+)[-\w]*)'
matches = re.findall(pattern, content)

for title, url, article_id in matches:
    # Clean up the title - remove "Intercom" placeholders and use URL slug if needed
    if title.strip() == 'Intercom':
        # Extract title from URL slug
        slug = url.split('/')[-1]
        title = slug.replace('-', ' ').title()
    articles.append((title.strip(), url, article_id))

# Group by section
sections = {}
current_section = None
current_articles = []

for line in content.split('\n'):
    if line.startswith('## ') and not line.startswith('## FAQ') and not line.startswith('## Intercom'):
        if current_section and current_articles:
            sections[current_section] = current_articles
        current_section = line[3:].strip()
        current_articles = []
    elif line.startswith('### ') and current_section:
        title = line[4:].strip()
        # Find the URL for this article
        url = None
        for t, u, aid in articles:
            if t == title or (title == 'Intercom' and t != 'Intercom'):
                url = u
                break
        if not url:
            url = 'N/A'
        current_articles.append((title, url))

if current_section and current_articles:
    sections[current_section] = current_articles

# Write index
with open('/root/.openclaw/workspace/bsport_article_index.md', 'w', encoding='utf-8') as f:
    f.write('# bsport Help Center — Article Index\n\n')
    f.write(f'> Total articles: {len(articles)}\n')
    f.write(f'> Generated: 2026-05-15\n\n')
    f.write('Use Ctrl+F to search this index, then look up the article in the full PDF.\n\n')
    f.write('---\n\n')
    
    for section, article_list in sections.items():
        if not article_list:
            continue
        # Skip weird sections that aren't real categories
        if any(x in section.lower() for x in ['step ', 'case:', 'on the ', 'pass credits', 'viewing and', 'why did', 'how to manage', 'understanding', 'managing', 'general tips', 'page overview', 'adding an', 'viewing availability', 'removing an', 'managing overlaps', 'multi-teacher', 'using filters', 'need help?', 'let\'s get started', 'scanner configuration', 'staff configuration', 'learn how to set up', 'connect bsport to', 'create a group', 'create a user', 'get the api key', 'if you are a franchise', 'choose your security', 'geofencing', 'proximity proof', 'set up your passes', 'entry based on', 'access control logic', 'the member can enter', 'localisation', 'checking on', 'valid status', 'warning status', 'acknowledge', 'indicate if', 'not valid status', 'access history', 'set up the validity', 'activation', 'first booking', 'manual activation', 'unlock a door', 'goefencing', 'check on a member', 'searching for a member', 'our tip', 'set up on kisi', 'controller', 'reader', 'other cases', 'delivery time', 'introduction', 'spanish electronic', 'why is this required', 'set up the integration', 'activate sequential', 'provide studio', 'social collaboration', 'invoice eligibility', 'invoice signature', 'failed invoice', 'successful invoice', 'in call cases', 'invoices finalized', 'reverse (refund)', 'activating fiskaly', 'what happens when', 'where to find', 'in case of an audit', 'frequently asked questions', 'what is sequential', 'who needs to set', 'where to set up', 'choose when', 'option 1', 'option 2', 'using an external', 'all set', 'prerequisites', 'detailed explanation', 'total due', 'payment received', 'payment planned', 'payment pending', 'payment outstanding', 'example', 'additional information', 'steps to export', 'expected result', 'what\'s inside', 'one pdf per', 'a csv file', 'documents downloaded', 'limitations', 'good to know', 'common error', 'overview of payment', 'handling unpaid', 'managing payment', 'resolving common', 'overview of sepa', 'disabling sepa', 'managing sepa for', 'implications of', 'ai for', 'what is ai', 'how to use', 'use cases', 'countdown timer', 'what is the countdown', 'company-saved', 'what are company', 'image gallery', 'saved uploads', 'what is it', 'general structure', 'start a new thread', 'actions on threads', 'filter and search', 'details section', '1st part', '2nd part', 'what is the purpose', 'how to get it', 'how to create', 'cash-based', 'accrual-based', 'why our purchases', 'all reports page', 'report detail page', 'advanced filters', 'date and quick', 'delete a view', 'compare reports', 'option 2: member side', 'hostinger', 'goal', 'sending a campaign', 'franchisee email', 'custom email domain', 'sending logic', 'all members campaign', 'smartlist filtering', 'select a sending studio', 'why a d-u-n-s', 'what is a d-u-n-s', 'why you need', 'google developer', 'apple developer program', 'steps to obtain', 'important country', 'troubleshooting d-u-n-s', 'next steps', 'why is google', 'step-by-step guide for', 'what to do if', 'step-by-step guide to', 'first: watch', 'then: follow', 'step 1: log in', 'step 2: access', 'step 3: choose', 'step 4: add', 'step 5: add', 'step 6: wait', 'step 7: confirm', 'step 8: finalize', 'troubleshooting tips', 'need help', 'create a google cloud', 'create the service', 'create \u0026 download', 'create the api', 'google api enablement', 'final check', 'that\'s it', 'need help', 'create an apple id', 'enroll in the', 'pay the', 'activate your', 'invite us as admin', 'how to invite', 'who can do this', 'before you start', 'after submission', 'google play', 'apple app store']):
            continue
        if len(section) > 60:  # Skip long sub-section headers
            continue
            
        f.write(f'## {section}\n\n')
        for title, url in article_list:
            if title == 'Intercom':
                # Try to extract from URL
                slug = url.split('/')[-1] if url != 'N/A' else 'unknown'
                title = slug.replace('-', ' ').title()
            f.write(f'- [{title}]({url})\n')
        f.write('\n')

print(f"Index created with {len(articles)} articles")
