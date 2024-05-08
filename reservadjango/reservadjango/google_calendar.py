import os.path
import datetime as dt
from pytz import timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarManager:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
    
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("client_secret_app_escritorio_oauth.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open ("token.json", 'w') as token:
                token.write(creds.to_json())

        return build("calendar", 'v3', credentials=creds)
    
    def list_busy_available_events(self, date, max_results=20):
        uy_timezone = timezone('America/Argentina/Buenos_Aires')
        date_str = date.strftime('%Y-%m-%d')
        selected_date = dt.datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=uy_timezone)
        tomorrow = (selected_date + dt.timedelta(days=1)).replace(hour=23, minute=59, second=0)
        
        hours = []
        
        day_of_week = selected_date.weekday()
        if day_of_week == 6: # DOMINGO
            hours = []
        else:
            current_time = dt.datetime.now(uy_timezone)
            if selected_date.date() == current_time.date():
                if current_time.hour > 19:
                    hours = []
                elif current_time.hour == 19 and current_time.minute >= 0:
                    hours = []
    
                else:
                    if current_time.hour < 10:
                        next_half_hour = current_time.replace(hour=10, minute=0, second=0)
                    else:
                        next_half_hour = current_time + dt.timedelta(minutes=(30 - current_time.minute % 30))
                
                        # Si next_half_hour es posterior a las 18:30, establecer hours como vacío
                        if next_half_hour.hour >= 19:
                            hours = []
                
                    # Generar las horas disponibles
                    hours = [next_half_hour.strftime('%H:%M')]
                    while next_half_hour.hour < 19 and (next_half_hour.hour < 18 or next_half_hour.minute < 30):
                        next_half_hour += dt.timedelta(minutes=30)
                        hours.append(next_half_hour.strftime('%H:%M'))
            else:
                hours = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30']

        events_result = self.service.events().list(calendarId='primary',
                                                   timeMin=selected_date.isoformat(), timeMax=tomorrow.isoformat(),
                                                   maxResults=max_results,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items',[])
        busy_hours = []

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start.replace('Z', '+00:00')
            start_datetime = dt.datetime.fromisoformat(start)
            if 'dateTime' in event['start']:
                busy_hours.append(start_datetime.strftime('%H:%M'))
        
        available_hours = [hour for hour in hours if hour not in busy_hours]

        return busy_hours, available_hours

    
    def create_event(self, summary, start_time, end_time, timezone='America/Argentina/Buenos_Aires'):
        event = {
            'summary': summary,
            'start': {
                'dateTime':start_time,
                'timeZone':timezone,
            },
            'end':{
                'dateTime':end_time,
                'timeZone':timezone,
            }
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Evento creado exitosamente: {event.get('htmlLink')}")
            return 200
        except HttpError as error:
            print(f"Ocurrio un error: {error}")

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        event = self.calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
        if summary:
            event['summary'] = summary

        if start_time:
            event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')

        if end_time:
            event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        updated_event = self.calendar_service.events().update(
            calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event

    def delete_event(self, event_id):
        self.calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True
    
calendar = GoogleCalendarManager()