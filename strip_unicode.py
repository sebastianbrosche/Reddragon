import re

with open('/root/.openclaw/workspace/bsport_help_center_clean.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace common Unicode characters with ASCII equivalents
replacements = {
    '⚠': 'WARNING:',
    '✅': '[YES]',
    '❌': '[NO]',
    '🔥': '[IMPORTANT]',
    '✍': '[NOTE]',
    '🖤': '[HEART]',
    '❤': '[HEART]',
    '‍': '',  # Zero-width joiner
    '️': '',  # Variation selector
    '📊': '[DATA]',
    '⚡': '[FAST]',
    '➡': '->',
    '✓': '[OK]',
    '✔': '[OK]',
    '→': '->',
    '←': '<-',
    '–': '-',
    '—': '--',
    ''': "'",
    ''': "'",
    '"': '"',
    '"': '"',
    '…': '...',
    '•': '*',
    '·': '*',
    '°': 'deg',
    '€': 'EUR',
    '£': 'GBP',
    '¥': 'JPY',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Remove any remaining non-ASCII characters (except newlines and common punctuation)
# Keep only ASCII range 32-126, plus tab and newline
content = ''.join(c if ord(c) < 128 or c in '\n\t\r' else ' ' for c in content)

# Clean up multiple spaces
content = re.sub(r' +', ' ', content)
content = re.sub(r'\n \n', '\n\n', content)
content = re.sub(r'\n{3,}', '\n\n', content)

with open('/root/.openclaw/workspace/bsport_help_center_ascii.md', 'w', encoding='ascii') as f:
    f.write(content)

print(f"Done! Output: {len(content)} characters")
