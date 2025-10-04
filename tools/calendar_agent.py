# tools/calendar_agent.py
import datetime as dt
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CalendarAgent:
    def __init__(self, credentials_path="credentials.json", token_path="token.json"):
        creds = None
        
        try:
            if os.path.exists(token_path) and os.path.getsize(token_path) > 0:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except json.JSONDecodeError:
            creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=8585)
            
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def check_availability(self, query: str) -> str:
        now = dt.datetime.now(dt.timezone.utc)
        end_time = now + dt.timedelta(days=7)
        events_result = self.service.events().list(
            calendarId="primary", timeMin=now.isoformat(), timeMax=end_time.isoformat(),
            singleEvents=True, orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        if not events: return "You have no upcoming events in the next 7 days."
        
        event_list = "\n".join(
            [f"- '{e['summary']}' on {dt.datetime.fromisoformat(e['start'].get('dateTime')).strftime('%Y-%m-%d at %H:%M')}" for e in events]
        )
        return f"Upcoming events:\n{event_list}"