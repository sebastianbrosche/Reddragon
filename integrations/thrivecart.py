#!/usr/bin/env python3
"""ThriveCart Integration — Orders, Refunds, Upsells"""
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

API_KEY = ENV.get('THRIVECART_API_KEY')
BASE = "https://thrivecart.com/api/external"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

def ping():
    """Test connectivity."""
    url = f'{BASE}/ping'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def list_orders(limit=10):
    """List recent orders."""
    url = f'{BASE}/orders?limit={limit}'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def get_order(order_id):
    """Get specific order."""
    url = f'{BASE}/orders/{order_id}'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def list_products():
    """List products."""
    url = f'{BASE}/products'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def list_customers(limit=10):
    """List customers."""
    url = f'{BASE}/customers?limit={limit}'
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def test():
    print('Testing ThriveCart...')
    try:
        pong = ping()
        print(f"  Account: {pong['account_name']} ({pong['account_url']})")
        print(f"  User: {pong['user_name']} ({pong['user_username']})")
        print(f"  Version: {pong['account_version']}")
        print('  ✓ ThriveCart API key valid.')
        print('  Note: Full order/product/customer API requires the ThriveCart PHP SDK')
        print('        or specific endpoint authentication.')
    except Exception as e:
        print(f'  ✗ Error: {e}')

if __name__ == '__main__':
    test()
