from calendar import monthrange
import datetime
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow()
    first_day = now.replace(day=1, hour=0, minute=0, second=0)
    last_day = now.replace(day=monthrange(now.year, now.month)[1], hour=23, minute=59, second=59)

    time_min = first_day.isoformat() + 'Z'
    time_max = last_day.isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=time_min, timeMax=time_max,
        maxResults=100, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])
    return [f"{e['start'].get('dateTime', e['start'].get('date'))} - {e['summary']}" for e in events]
