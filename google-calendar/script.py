from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to service account JSON file
SERVICE_ACCOUNT_FILE = "credentials.json"

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Authenticate and build service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

timenow = datetime.now()
time_ahead_one_day = timenow + timedelta(days=1)
# Define event details
event = {
    "summary": "Meeting with Team",
    "location": "Google Meet",
    "description": "Discussion about project updates.",
    "start": {
        "dateTime": (time_ahead_one_day).isoformat(),
        "timeZone": "Asia/Kolkata",
    },
    "end": {
        "dateTime": (time_ahead_one_day + timedelta(days=1, hours=1)).isoformat(),
        "timeZone": "Asia/Kolkata",
    },
    "attendees": [
        {"email": "1999.ayush.srivastava@vimaan.ai"},
        {"email": "ayushclashofclans1@gmail.com"},
    ],
    "reminders": {
        "useDefault": False,
        "overrides": [
            {"method": "email", "minutes": 24 * 60},
            {"method": "popup", "minutes": 10},
        ],
    },
}

# Insert event into the calendar
event_result = service.events().insert(calendarId="4d8439995ddc377324c310be7ba383cdc5c9377b90b19759f04138e23b7e6b64@group.calendar.google.com", body=event).execute()
print("Event created:", event_result.get("htmlLink"))
