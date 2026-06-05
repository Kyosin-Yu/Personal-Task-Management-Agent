import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_services():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def add_calendar_event(title, description, due_date, due_time=None):
    try:
        service = get_calendar_services()

        if due_time:
            start_datetime = f"{due_date}T{due_time}:00"
            end_datetime = f"{due_date}T{due_time}:00"
            event = {
                "summary": title,
                "description": description,
                "start": {
                    "date": due_date,
                    "timeZone": "Asia/Kuala_Lumpur",
                },
                "end": {
                    "date": due_date,
                    "timeZone": "Asia/Kuala_Lumpur",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 30},
                    ]
                }
            }
        else:
            event = {
                "summary": title,
                "description": description,
                "start": {
                    "date": due_date,
                    "timeZone": "Asia/Kuala_Lumpur",
                },
                "end": {
                    "date": due_date,
                    "timeZone": "Asia/Kuala_Lumpur",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 60},
                    ]
                }
            }

        event = service.events().insert(
            calendarId="primary", body=event
        ).execute()

        return f"Calendar Event created: {event.get('htmlLink')}"
    except Exception as e:
        return f"Calendar Sync Failed: {str(e)}"

def delete_calendar_event(title):
    try:
        service = get_calendar_services()

        events_result = service.events().list(
            calendarId="primary",
            q=title,
            maxResults=5,
            singleEvents=True,
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return "-- No matching events found --"

        for event in events:
            if title.lower() in event["summary"].lower():
                service.events().delete(calendarId="primary",
                                        eventId=event["id"]
                ).execute()
                return f"Calendar Event deleted: {event['summary']}"

        return "-- No matching events found --"
    except Exception as e:
        return f"Calendar Sync Failed: {str(e)}"

def get_upcoming_events():
    try:
        service = get_calendar_services()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return "-- No upcoming events found --"

        result = "== Upcoming Events ==\n"
        for event in events:
            start = event["start"].get("date", event["start"].get("dateTime", ""))
            result += f"- {event['summary']} on {start}\n"

        return result
    except Exception as e:
        return f"Failed to fetch events: {str(e)}"
