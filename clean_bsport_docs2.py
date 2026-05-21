from bs4 import BeautifulSoup
import re

# Read the raw file
with open('/root/.openclaw/workspace/bsport_help_center.md', 'r', encoding='utf-8') as f:
    raw_content = f.read()

# Better approach: Parse the raw markdown and extract articles
# Each article starts with "### " and ends before the next "### " or "## "

sections = []
current_section = None
current_articles = []

# Split by lines and process
lines = raw_content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for section header
    if line.startswith('## '):
        if current_section and current_articles:
            sections.append((current_section, current_articles))
        current_section = line[3:].strip()
        current_articles = []
        i += 1
        continue
    
    # Check for article header
    if line.startswith('### '):
        title = line[4:].strip()
        i += 1
        
        # Get URL
        url = ''
        if i < len(lines) and lines[i].startswith('**URL:**'):
            url = lines[i][8:].strip()
            i += 1
        
        # Get HTML content until next article or section
        html_content = []
        while i < len(lines):
            if lines[i].startswith('### ') or lines[i].startswith('## ') or lines[i] == '---':
                break
            if lines[i].strip():
                html_content.append(lines[i])
            i += 1
        
        if html_content:
            html = '\n'.join(html_content)
            current_articles.append((title, url, html))
    else:
        i += 1

if current_section and current_articles:
    sections.append((current_section, current_articles))

# Now clean up and write
output = '# bsport Complete Help Center Documentation\n\n'
output += '> Compiled from https://intercom.help/bsport-helpcenter/en\n'
output += '> Total sections: ' + str(len(sections)) + '\n'
output += '> Generated: ' + __import__('datetime').datetime.now().isoformat() + '\n\n'

total_articles = 0

for section_name, articles in sections:
    if not articles:
        continue
    
    output += f'\n## {section_name}\n\n'
    
    for title, url, html in articles:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to get real title from h1 in the content
        h1 = soup.find('h1')
        if h1:
            real_title = h1.get_text().strip()
            if real_title and real_title != 'Intercom':
                title = real_title
        
        # Extract text content
        text_parts = []
        for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'b', 'strong']):
            text = elem.get_text().strip()
            if text and len(text) > 2:
                # Skip image captions and empty paragraphs
                if elem.name in ['h1', 'h2']:
                    text_parts.append(f'\n## {text}\n')
                elif elem.name == 'h3':
                    text_parts.append(f'\n### {text}\n')
                elif elem.name == 'h4':
                    text_parts.append(f'\n#### {text}\n')
                elif elem.name == 'li':
                    text_parts.append(f'- {text}')
                else:
                    text_parts.append(text)
        
        text_content = '\n'.join(text_parts)
        # Clean up excessive newlines
        text_content = re.sub(r'\n{3,}', '\n\n', text_content)
        
        if len(text_content.strip()) > 30:
            output += f'### {title}\n'
            output += f'**Source:** {url}\n\n'
            output += text_content.strip() + '\n\n'
            output += '---\n\n'
            total_articles += 1

output += f'\n\n---\n\n*Total articles compiled: {total_articles}*\n'

with open('/root/.openclaw/workspace/bsport_help_center_clean.md', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Done! Compiled {total_articles} articles from {len(sections)} sections')
print(f'Output size: {len(output)} characters')
