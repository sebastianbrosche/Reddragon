from bs4 import BeautifulSoup
import re

# Read the raw file
with open('/root/.openclaw/workspace/bsport_help_center.md', 'r', encoding='utf-8') as f:
    raw_content = f.read()

# Split into sections
sections = re.split(r'(?=## [^\n]+\n)', raw_content)

clean_output = '# bsport Complete Help Center Documentation\n\n'
clean_output += '> Compiled from https://intercom.help/bsport-helpcenter/en\n'
clean_output += '> Total articles: ~609 across 16 sections\n'
clean_output += '> Generated: Auto-compiled\n\n'

article_count = 0

for section in sections:
    section_match = re.match(r'## ([^\n]+)', section)
    if section_match:
        clean_output += f'\n## {section_match.group(1)}\n\n'
    
    # Find all article blocks
    # Pattern: ### Title followed by **URL:** then HTML content
    articles = re.findall(
        r'### ([^\n]+)\n\*\*URL:\*\* ([^\n]+)\n\n(<div class="intercom-interblocks.*?(?=(?:### |## |$)))',
        section,
        re.DOTALL
    )
    
    for title, url, html in articles:
        if 'Intercom' in title and 'bsport - Help Center' in title:
            # Try to get title from the HTML content instead
            soup = BeautifulSoup(html, 'html.parser')
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text().strip()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract text content
        text_parts = []
        for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'strong', 'em']):
            text = elem.get_text().strip()
            if text:
                if elem.name == 'h1':
                    text_parts.append(f'\n# {text}\n')
                elif elem.name == 'h2':
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
        text_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', text_content)
        
        if len(text_content.strip()) > 50:
            clean_output += f'### {title}\n'
            clean_output += f'**Source:** {url}\n\n'
            clean_output += text_content.strip() + '\n\n'
            clean_output += '---\n\n'
            article_count += 1

with open('/root/.openclaw/workspace/bsport_help_center_clean.md', 'w', encoding='utf-8') as f:
    f.write(clean_output)

print(f'Done! Cleaned {article_count} articles')
print(f'File size: {len(clean_output)} chars')
