
from datetime import datetime, timedelta, date
import os
import pickle
from random import randrange
import time

import zoneinfo
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def calendar_update(message: str, day: int, retry: bool = True, backoff_factor: int = 2):
    starting_date = date(2025, 3, 12) + timedelta(days=day)
    event = {
        "summary": f"{message}",
        "location": "Our Happy Place",
        "description": "Gentle reminder on how awesome you are, please don't doubt yourself! 🌕😘❤️",
        "start": {
            "date": (starting_date).isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "date": (starting_date + timedelta(days=1)).isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "attendees": [{"email": "1999.ayush.srivastava@gmail.com"}, {"email": "akritidpsg11@gmail.com"}],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 16 * 60},  # 8 AM on the event day
                {"method": "email", "minutes": 16 * 60},
            ],
        },
    }
    while True:
        try:
            # service.events().insert(calendarId="primary", body=event).execute()
            event_result = service.events().insert(calendarId="primary", body=event).execute()
            print("Event created:", event_result.get("htmlLink"))
            break
        except Exception as e:
            if retry:
                print(f"Error: {e}")
                print(f"Retrying after {backoff_factor} seconds...")
                time.sleep(backoff_factor)
                backoff_factor *= 2
            else:
                raise

# read json file
with open('events.json', 'r') as file:
    data = json.load(file)

# print(data['morning'])
tz = zoneinfo.ZoneInfo('Asia/Kolkata')
# Load or authenticate credentials
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file("credentials-oauth.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

service = build("calendar", "v3", credentials=creds)

# Create event with attendees
day = 0
while data['morning']:
    print("Iteration: ", day)
    item_number = randrange(len(data['morning']))
    i = data['morning'].pop(item_number)
    print(i)

    calendar_update(i, day)
    day += 1
    time.sleep(10)

print("Done")
