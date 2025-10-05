from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from typing import List, Dict

def create_calendar_event(
    credentials: Credentials,
    title: str,
    start_time: datetime,
    description: str = "",
    duration_minutes: int = 60,
    calendar_id: str = 'primary'
) -> Dict:
    """
    Create a calendar event
    
    Args:
        credentials: Google OAuth credentials
        title: Event title
        start_time: Event start datetime
        description: Event description
        duration_minutes: Event duration in minutes
        calendar_id: Calendar ID (default: 'primary')
    
    Returns:
        Created event dictionary
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        
        # Calculate end time
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Event body
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Tashkent',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Tashkent',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        
        # Create event
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
        return event
        
    except Exception as e:
        print(f"Error creating calendar event: {e}")
        raise

def get_user_calendars(credentials: Credentials) -> List[Dict]:
    """
    Get list of user's calendars
    
    Args:
        credentials: Google OAuth credentials
    
    Returns:
        List of calendar dictionaries
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        
        calendar_list = service.calendarList().list().execute()
        
        calendars = []
        for calendar in calendar_list.get('items', []):
            calendars.append({
                'id': calendar['id'],
                'summary': calendar['summary'],
                'primary': calendar.get('primary', False),
                'accessRole': calendar.get('accessRole')
            })
        
        return calendars
        
    except Exception as e:
        print(f"Error fetching calendars: {e}")
        raise

def get_upcoming_events(
    credentials: Credentials,
    max_results: int = 10,
    calendar_id: str = 'primary'
) -> List[Dict]:
    """
    Get upcoming calendar events
    
    Args:
        credentials: Google OAuth credentials
        max_results: Maximum number of events to return
        calendar_id: Calendar ID (default: 'primary')
    
    Returns:
        List of event dictionaries
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get current time in RFC3339 format
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        return events
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        raise

def update_calendar_event(
    credentials: Credentials,
    event_id: str,
    title: str = None,
    start_time: datetime = None,
    description: str = None,
    calendar_id: str = 'primary'
) -> Dict:
    """
    Update an existing calendar event
    
    Args:
        credentials: Google OAuth credentials
        event_id: Event ID to update
        title: New event title (optional)
        start_time: New start time (optional)
        description: New description (optional)
        calendar_id: Calendar ID (default: 'primary')
    
    Returns:
        Updated event dictionary
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        
        # Get existing event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        # Update fields if provided
        if title:
            event['summary'] = title
        
        if description is not None:
            event['description'] = description
        
        if start_time:
            duration = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00')) - \
                      datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            
            event['start']['dateTime'] = start_time.isoformat()
            event['end']['dateTime'] = (start_time + duration).isoformat()
        
        # Update event
        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event
        ).execute()
        
        return updated_event
        
    except Exception as e:
        print(f"Error updating event: {e}")
        raise

def delete_calendar_event(
    credentials: Credentials,
    event_id: str,
    calendar_id: str = 'primary'
) -> bool:
    """
    Delete a calendar event
    
    Args:
        credentials: Google OAuth credentials
        event_id: Event ID to delete
        calendar_id: Calendar ID (default: 'primary')
    
    Returns:
        True if successful
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        
        return True
        
    except Exception as e:
        print(f"Error deleting event: {e}")
        raise