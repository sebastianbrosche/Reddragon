#!/usr/bin/env python3
"""Cloudflare Integration — Pages + DNS"""
import requests
from pathlib import Path

def load_env():
    creds = {}
    path = Path('/root/.openclaw/workspace/.credentials.env')
    if path.exists():
        for line in path.read_text().splitlines():
            if line.startswith('#') or not line.strip() or '=' not in line:
                continue
            k, v = line.split('=', 1)
            creds[k.strip()] = v.strip()
    return creds

ENV = load_env()

API_TOKEN = ENV.get('CLOUDFLARE_API_TOKEN')
ACCOUNT_ID = ENV.get('CLOUDFLARE_ACCOUNT_ID')
ZONE_ID = ENV.get('CLOUDFLARE_ZONE_ID')

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def list_pages_projects():
    """List all Pages projects."""
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def get_page_project(name):
    """Get specific Pages project."""
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{name}'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def list_dns_records():
    """List DNS records for the zone."""
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def get_zone_details():
    """Get zone info."""
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def test():
    print('Testing Cloudflare...')
    try:
        zone = get_zone_details()
        print(f"  Zone: {zone['result']['name']} ({zone['result']['status']})")
        
        pages = list_pages_projects()
        for p in pages.get('result', []):
            print(f"  Pages project: {p['name']} ({p.get('subdomain', 'no-sub')})")
        
        dns = list_dns_records()
        print(f"  DNS records: {len(dns.get('result', []))}")
        print('  ✓ Cloudflare connected.')
    except Exception as e:
        print(f'  ✗ Error: {e}')

if __name__ == '__main__':
    test()
