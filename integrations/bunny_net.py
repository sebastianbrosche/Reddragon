#!/usr/bin/env python3
"""Bunny.net Video CDN Integration — 3 Libraries"""
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

LIBRARIES = {
    'yogaforbjj': {
        'id': ENV.get('BUNNY_LIB1_ID', '215008'),
        'api_key': ENV.get('BUNNY_LIB1_API_KEY'),
        'cdn': ENV.get('BUNNY_LIB1_CDN', 'vz-5ecbf445-fd1.b-cdn.net'),
    },
    'courses': {
        'id': ENV.get('BUNNY_LIB2_ID', '220256'),
        'api_key': ENV.get('BUNNY_LIB2_API_KEY'),
        'cdn': ENV.get('BUNNY_LIB2_CDN', 'vz-58c3981c-cce.b-cdn.net'),
    },
    'ads': {
        'id': ENV.get('BUNNY_LIB3_ID', '401774'),
        'api_key': ENV.get('BUNNY_LIB3_API_KEY'),
        'cdn': ENV.get('BUNNY_LIB3_CDN', 'vz-76b2c0b8-3d1.b-cdn.net'),
    }
}

BASE = "https://video.bunnycdn.com/Library"

def list_videos(lib_name='yogaforbjj', page=1, per_page=100):
    """List videos in a library."""
    lib = LIBRARIES[lib_name]
    headers = {'AccessKey': lib['api_key']}
    url = f"{BASE}/{lib['id']}/Videos?page={page}&itemsPerPage={per_page}"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def get_video(lib_name, video_id):
    """Get video details."""
    lib = LIBRARIES[lib_name]
    headers = {'AccessKey': lib['api_key']}
    url = f"{BASE}/{lib['id']}/Videos/{video_id}"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def search_videos(lib_name, query):
    """Search videos by title."""
    lib = LIBRARIES[lib_name]
    headers = {'AccessKey': lib['api_key']}
    url = f"{BASE}/{lib['id']}/Videos?search={requests.utils.quote(query)}"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def get_video_url(lib_name, video_guid):
    """Get direct playback URL."""
    lib = LIBRARIES[lib_name]
    return f"https://{lib['cdn']}/{video_guid}/playlist.m3u8"

def get_thumbnail(lib_name, video_guid):
    """Get thumbnail URL."""
    lib = LIBRARIES[lib_name]
    return f"https://{lib['cdn']}/{video_guid}/{video_guid}_thumbnail.jpg"

# --- Stats ---

def get_library_stats(lib_name='yogaforbjj'):
    """Get library analytics (views, bandwidth, etc)."""
    lib = LIBRARIES[lib_name]
    headers = {'AccessKey': lib['api_key']}
    url = f"{BASE}/{lib['id']}/Statistics"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def test_all():
    print("Testing Bunny.net...")
    for name, lib in LIBRARIES.items():
        print(f"\n📚 Library: {name} (ID: {lib['id']})")
        try:
            result = list_videos(name, per_page=5)
            items = result.get('items', [])
            print(f"  Videos: {result.get('totalItems', 0)}")
            for v in items[:3]:
                print(f"    - {v.get('title', 'Untitled')} ({v.get('guid', 'no-guid')})")
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == '__main__':
    test_all()
