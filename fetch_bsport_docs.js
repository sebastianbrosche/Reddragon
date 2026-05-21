const fs = require('fs');
const https = require('https');

// Collection URLs and names
const collections = [
  { name: "FAQ", url: "https://intercom.help/bsport-helpcenter/en/collections/2348836-frequently-asked-questions", count: 10 },
  { name: "FAQ-Members", url: "https://intercom.help/bsport-helpcenter/en/collections/2348822-faq-members", count: 29 },
  { name: "Dashboard", url: "https://intercom.help/bsport-helpcenter/en/collections/3868459-dashboard", count: 4 },
  { name: "Calendar", url: "https://intercom.help/bsport-helpcenter/en/collections/3868464-calendar", count: 39 },
  { name: "Schedule", url: "https://intercom.help/bsport-helpcenter/en/collections/3868465-schedule", count: 6 },
  { name: "Access-Control", url: "https://intercom.help/bsport-helpcenter/en/collections/11843931-access-control", count: 9 },
  { name: "My-Studio", url: "https://intercom.help/bsport-helpcenter/en/collections/3868469-my-studio", count: 56 },
  { name: "Products", url: "https://intercom.help/bsport-helpcenter/en/collections/3868488-products", count: 80 },
  { name: "Transactions", url: "https://intercom.help/bsport-helpcenter/en/collections/3868505-transactions", count: 31 },
  { name: "Marketing", url: "https://intercom.help/bsport-helpcenter/en/collections/3868518-marketing", count: 85 },
  { name: "Inbox", url: "https://intercom.help/bsport-helpcenter/en/collections/5756407-inbox", count: 3 },
  { name: "Members", url: "https://intercom.help/bsport-helpcenter/en/collections/3868533-members", count: 75 },
  { name: "Reporting", url: "https://intercom.help/bsport-helpcenter/en/collections/3868534-reporting", count: 28 },
  { name: "Settings", url: "https://intercom.help/bsport-helpcenter/en/collections/3868535-settings", count: 133 },
  { name: "Master-Account", url: "https://intercom.help/bsport-helpcenter/en/collections/4044927-master-account", count: 5 },
  { name: "Branded-App", url: "https://intercom.help/bsport-helpcenter/en/collections/8575557-branded-app", count: 16 }
];

// Function to fetch a URL
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Extract article URLs from collection page
function extractArticleUrls(html) {
  const urls = [];
  const regex = /https:\/\/intercom\.help\/bsport-helpcenter\/en\/articles\/[\d-]+[a-z0-9-]*/g;
  let match;
  while ((match = regex.exec(html)) !== null) {
    if (!urls.includes(match[0])) {
      urls.push(match[0]);
    }
  }
  return urls;
}

// Main function
async function main() {
  let output = '# bsport Complete Help Center Documentation\n\n';
  output += '> Compiled from https://intercom.help/bsport-helpcenter/en\n';
  output += '> Total articles: ~609 across 16 sections\n\n';
  output += '---\n\n';

  for (const collection of collections) {
    console.log(`Processing: ${collection.name}...`);
    try {
      const html = await fetchUrl(collection.url);
      const articleUrls = extractArticleUrls(html);
      
      output += `## ${collection.name} (${articleUrls.length} articles)\n\n`;
      
      for (const articleUrl of articleUrls.slice(0, 20)) { // Limit to 20 per section for now
        try {
          const articleHtml = await fetchUrl(articleUrl);
          // Extract title
          const titleMatch = articleHtml.match(/<title>([^<]*)<\/title>/);
          const title = titleMatch ? titleMatch[1].replace(' | bsport - Help Center', '') : 'Untitled';
          
          // Extract main content (simplified)
          const contentMatch = articleHtml.match(/<article[^>]*>([\s\S]*?)<\/article>/);
          const content = contentMatch ? contentMatch[1] : 'Content not available';
          
          output += `### ${title}\n`;
          output += `**URL:** ${articleUrl}\n\n`;
          output += `${content}\n\n`;
          output += '---\n\n';
          
          // Small delay to be polite
          await new Promise(r => setTimeout(r, 500));
        } catch (e) {
          console.error(`Error fetching ${articleUrl}: ${e.message}`);
        }
      }
    } catch (e) {
      console.error(`Error processing ${collection.name}: ${e.message}`);
    }
  }

  fs.writeFileSync('/root/.openclaw/workspace/bsport_help_center.md', output);
  console.log('Done! Saved to bsport_help_center.md');
}

main().catch(console.error);
