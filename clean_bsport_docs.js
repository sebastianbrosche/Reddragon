const fs = require('fs');

// Read the raw file
const rawContent = fs.readFileSync('/root/.openclaw/workspace/bsport_help_center.md', 'utf8');

// Simple HTML tag remover
function stripHtml(html) {
  return html
    .replace(/<[^\u003e]+>/g, '')
    .replace(/\u0026amp;/g, '&')
    .replace(/\u0026lt;/g, '<')
    .replace(/\u0026gt;/g, '>')
    .replace(/\u0026quot;/g, '"')
    .replace(/\u0026#x27;/g, "'")
    .replace(/\u0026nbsp;/g, ' ')
    .replace(/\n\s*\n\s*\n/g, '\n\n')
    .trim();
}

// Split by article sections
const sections = rawContent.split(/(?=## [^\n]+\n)/);

let cleanOutput = '# bsport Complete Help Center Documentation\n\n';
cleanOutput += '> Compiled from https://intercom.help/bsport-helpcenter/en\n';
cleanOutput += '> Total articles: ~609 across 16 sections\n';
cleanOutput += '> Generated: ' + new Date().toISOString() + '\n\n';

let articleCount = 0;

for (const section of sections) {
  // Check if it's a section header
  const sectionMatch = section.match(/^## ([^\n]+)/);
  if (sectionMatch) {
    cleanOutput += `\n## ${sectionMatch[1]}\n\n`;
  }
  
  // Extract articles within this section
  const articles = section.split(/(?=### [^\n]+\n)/);
  
  for (const article of articles) {
    const titleMatch = article.match(/^### ([^\n]+)/);
    if (!titleMatch) continue;
    
    const title = titleMatch[1];
    const urlMatch = article.match(/\*\*URL:\*\* ([^\n]+)/);
    const url = urlMatch ? urlMatch[1] : '';
    
    // Extract the HTML content block
    const htmlMatch = article.match(/(<div class="intercom-interblocks[^]*?<\/section>)/s);
    if (!htmlMatch) continue;
    
    const cleanText = stripHtml(htmlMatch[1]);
    if (cleanText.length > 50) {
      cleanOutput += `### ${title}\n`;
      cleanOutput += `**Source:** ${url}\n\n`;
      cleanOutput += cleanText + '\n\n';
      cleanOutput += '---\n\n';
      articleCount++;
    }
  }
}

cleanOutput += `\n\n---\n\n*Total articles compiled: ${articleCount}*\n`;

fs.writeFileSync('/root/.openclaw/workspace/bsport_help_center_clean.md', cleanOutput);
console.log(`Done! Cleaned ${articleCount} articles and saved to bsport_help_center_clean.md`);
console.log(`File size: ${(fs.statSync('/root/.openclaw/workspace/bsport_help_center_clean.md').size / 1024).toFixed(2)} KB`);
