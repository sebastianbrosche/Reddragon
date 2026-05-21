#!/usr/bin/env bash
# Read IOM session logs from Cloudflare KV
# Usage: ./read-iom-logs.sh [limit]

LIMIT=${1:-50}
TOKEN="cfut_YKTQuAMClyldwvmASE2dtBZ3z0LzDOvrfemTdH7V21836a51"
ACCOUNT_ID="sebastian-brosche"  # From worker URL
NAMESPACE_ID="b3e5c14bebda4fae9446e468e8968025"

echo "=== IOM Session Logs (last $LIMIT entries) ==="
echo ""

# List keys from KV
curl -s "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/storage/kv/namespaces/$NAMESPACE_ID/keys?limit=$LIMIT" \
  -H "Authorization: Bearer $TOKEN" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    for key in data.get('result', []):
        print(key['name'])
else:
    print('Error:', data.get('errors', 'Unknown'))
"
