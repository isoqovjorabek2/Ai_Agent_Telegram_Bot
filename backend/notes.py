from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Dict, List

def create_keep_note(
    credentials: Credentials,
    title: str,
    content: str = ""
) -> Dict:
    """
    Create a Google Keep note
    
    Note: Google Keep API is limited. This implementation uses the Keep Notes API
    which may require additional setup. Alternatively, you can use gkeepapi library
    for unofficial access.
    
    Args:
        credentials: Google OAuth credentials
        title: Note title
        content: Note content
    
    Returns:
        Created note dictionary
    """
    try:
        # Using Google Keep API (if available)
        # Note: Official Keep API is not publicly available yet
        # This is a placeholder implementation
        
        service = build('keep', 'v1', credentials=credentials)
        
        note_body = {
            'title': title,
            'body': {
                'text': {
                    'text': content
                }
            }
        }
        
        note = service.notes().create(body=note_body).execute()
        
        return note
        
    except Exception as e:
        print(f"Error creating Keep note: {e}")
        # Fallback: Create as a task or use alternative method
        return create_keep_note_fallback(credentials, title, content)

def create_keep_note_fallback(
    credentials: Credentials,
    title: str,
    content: str
) -> Dict:
    """
    Fallback method: Create note using Google Tasks API
    (since Keep API is not publicly available)
    
    Args:
        credentials: Google OAuth credentials
        title: Note title
        content: Note content
    
    Returns:
        Created task dictionary
    """
    try:
        service = build('tasks', 'v1', credentials=credentials)
        
        task_body = {
            'title': title,
            'notes': content
        }
        
        # Create task in default task list
        task = service.tasks().insert(
            tasklist='@default',
            body=task_body
        ).execute()
        
        return {
            'name': task['id'],
            'title': task['title'],
            'notes': task.get('notes', ''),
            'status': task.get('status')
        }
        
    except Exception as e:
        print(f"Error creating task: {e}")
        raise

def list_keep_notes(credentials: Credentials, max_results: int = 10) -> List[Dict]:
    """
    List Keep notes (or tasks as fallback)
    
    Args:
        credentials: Google OAuth credentials
        max_results: Maximum number of notes to return
    
    Returns:
        List of note dictionaries
    """
    try:
        service = build('tasks', 'v1', credentials=credentials)
        
        results = service.tasks().list(
            tasklist='@default',
            maxResults=max_results
        ).execute()
        
        tasks = results.get('items', [])
        
        notes = []
        for task in tasks:
            notes.append({
                'id': task['id'],
                'title': task['title'],
                'content': task.get('notes', ''),
                'status': task.get('status'),
                'updated': task.get('updated')
            })
        
        return notes
        
    except Exception as e:
        print(f"Error listing notes: {e}")
        raise

def update_keep_note(
    credentials: Credentials,
    note_id: str,
    title: str = None,
    content: str = None
) -> Dict:
    """
    Update a Keep note (or task as fallback)
    
    Args:
        credentials: Google OAuth credentials
        note_id: Note ID to update
        title: New title (optional)
        content: New content (optional)
    
    Returns:
        Updated note dictionary
    """
    try:
        service = build('tasks', 'v1', credentials=credentials)
        
        # Get existing task
        task = service.tasks().get(
            tasklist='@default',
            task=note_id
        ).execute()
        
        # Update fields if provided
        if title:
            task['title'] = title
        
        if content is not None:
            task['notes'] = content
        
        # Update task
        updated_task = service.tasks().update(
            tasklist='@default',
            task=note_id,
            body=task
        ).execute()
        
        return {
            'id': updated_task['id'],
            'title': updated_task['title'],
            'content': updated_task.get('notes', ''),
            'status': updated_task.get('status')
        }
        
    except Exception as e:
        print(f"Error updating note: {e}")
        raise

def delete_keep_note(credentials: Credentials, note_id: str) -> bool:
    """
    Delete a Keep note (or task as fallback)
    
    Args:
        credentials: Google OAuth credentials
        note_id: Note ID to delete
    
    Returns:
        True if successful
    """
    try:
        service = build('tasks', 'v1', credentials=credentials)
        
        service.tasks().delete(
            tasklist='@default',
            task=note_id
        ).execute()
        
        return True
        
    except Exception as e:
        print(f"Error deleting note: {e}")
        raise

# Alternative: Using gkeepapi (unofficial library)
# Uncomment if you want to use the unofficial Keep API

"""
import gkeepapi

def create_keep_note_gkeepapi(email: str, app_password: str, title: str, content: str) -> Dict:
    '''
    Create note using gkeepapi (unofficial)
    Requires app password from Google Account
    '''
    try:
        keep = gkeepapi.Keep()
        keep.login(email, app_password)
        
        note = keep.createNote(title, content)
        keep.sync()
        
        return {
            'id': note.id,
            'title': note.title,
            'content': note.text
        }
    except Exception as e:
        print(f"gkeepapi error: {e}")
        raise
"""