import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Escopo de leitura da agenda
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def is_valid_token_file(filepath):
    """Verifica se o token.json está presente e contém JSON válido."""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        return True
    except Exception:
        return False

def get_events():
    creds = None

    # Verifica se token.json existe e é válido
    if os.path.exists('token.json') and is_valid_token_file('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se não tiver credenciais válidas, faz login via navegador
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva o novo token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Conecta à API do Google Calendar
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(hours=23)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=end_of_day,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', '(Sem título)')
        event_list.append(f"{start} - {summary}")

    return event_list
