#!/usr/bin/env python3
"""
Google Workspace Integration for Miha
Handles Gmail, Drive, Calendar, Docs, YouTube, Search Console, GTM
"""
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load credentials from secure store
CREDS_PATH = Path('/root/.openclaw/workspace/.credentials.env')

def load_env_vars():
    """Parse the credentials env file."""
    vars = {}
    if CREDS_PATH.exists():
        for line in CREDS_PATH.read_text().splitlines():
            if line.startswith('#') or not line.strip() or '=' not in line:
                continue
            key, val = line.split('=', 1)
            vars[key.strip()] = val.strip()
    return vars

ENV = load_env_vars()

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/webmasters.readonly',
    'https://www.googleapis.com/auth/tagmanager.readonly',
]

def get_credentials():
    """Build credentials from stored refresh token."""
    creds = Credentials(
        token=None,
        refresh_token=ENV.get('GOOGLE_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=ENV.get('GOOGLE_CLIENT_ID'),
        client_secret=ENV.get('GOOGLE_CLIENT_SECRET'),
        scopes=SCOPES
    )
    # Refresh to get a valid access token
    creds.refresh(Request())
    return creds

def get_gmail_service():
    return build('gmail', 'v1', credentials=get_credentials())

def get_drive_service():
    return build('drive', 'v3', credentials=get_credentials())

def get_calendar_service():
    return build('calendar', 'v3', credentials=get_credentials())

def get_docs_service():
    return build('docs', 'v1', credentials=get_credentials())

def get_youtube_service():
    return build('youtube', 'v3', credentials=get_credentials())

def get_searchconsole_service():
    return build('webmasters', 'v3', credentials=get_credentials())

def get_gtm_service():
    return build('tagmanager', 'v2', credentials=get_credentials())

# --- Quick Test Functions ---

def test_gmail():
    """List last 5 messages."""
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    msgs = results.get('messages', [])
    return [m['id'] for m in msgs]

def test_drive():
    """List files in root."""
    service = get_drive_service()
    results = service.files().list(pageSize=5, fields="files(name, mimeType)").execute()
    return results.get('files', [])

def test_calendar():
    """List next 5 events."""
    service = get_calendar_service()
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    results = service.events().list(calendarId='primary', timeMin=now, maxResults=5, singleEvents=True, orderBy='startTime').execute()
    return results.get('items', [])

if __name__ == '__main__':
    print('Testing Google Workspace APIs...')
    try:
        creds = get_credentials()
        print(f'✓ Authenticated. Access token: {creds.token[:20]}...')
        
        print('\nGmail:', test_gmail())
        print('\nDrive:', test_drive())
        print('\nCalendar:', test_calendar())
        print('\n✓ All Google Workspace APIs connected.')
    except Exception as e:
        print(f'✗ Error: {e}')
