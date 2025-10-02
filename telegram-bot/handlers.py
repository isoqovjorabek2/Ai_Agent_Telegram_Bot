import re
from datetime import datetime, timedelta
from typing import Dict, Optional

# Uzbek and Russian date/time keywords
UZBEK_DAYS = {
    'bugun': 0, 'ertaga': 1, 'indinga': 2,
    'dushanba': 'monday', 'seshanba': 'tuesday', 'chorshanba': 'wednesday',
    'payshanba': 'thursday', 'juma': 'friday', 'shanba': 'saturday', 'yakshanba': 'sunday'
}

RUSSIAN_DAYS = {
    'сегодня': 0, 'завтра': 1, 'послезавтра': 2,
    'понедельник': 'monday', 'вторник': 'tuesday', 'среда': 'wednesday',
    'четверг': 'thursday', 'пятница': 'friday', 'суббота': 'saturday', 'воскресенье': 'sunday'
}

UZBEK_MONTHS = {
    'yanvar': 1, 'fevral': 2, 'mart': 3, 'aprel': 4, 'may': 5, 'iyun': 6,
    'iyul': 7, 'avgust': 8, 'sentabr': 9, 'oktabr': 10, 'noyabr': 11, 'dekabr': 12
}

RUSSIAN_MONTHS = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
    'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}

# Keywords for note detection
NOTE_KEYWORDS_UZ = ['eslatma', 'yozib qo', 'qayd et', 'unutma', 'eslatib qol']
NOTE_KEYWORDS_RU = ['заметка', 'запиши', 'записать', 'не забыть', 'напомни']

def parse_time(text: str) -> Optional[str]:
    """Extract time from text"""
    # Pattern: soat 14, 14:30, 14.30, в 14:00, kuni 10
    time_patterns = [
        r'(?:soat|в|kuni)\s*(\d{1,2})(?::(\d{2}))?',  # soat 14:30, в 14:00
        r'(\d{1,2}):(\d{2})',  # 14:30
        r'(\d{1,2})\.(\d{2})',  # 14.30
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text.lower())
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"
    
    return None

def parse_date(text: str) -> Optional[datetime]:
    """Extract date from text"""
    text_lower = text.lower()
    today = datetime.now()
    
    # Check for relative days (today, tomorrow)
    for word, offset in {**UZBEK_DAYS, **RUSSIAN_DAYS}.items():
        if isinstance(offset, int) and word in text_lower:
            return today + timedelta(days=offset)
    
    # Check for weekdays
    for word, day_name in {**UZBEK_DAYS, **RUSSIAN_DAYS}.items():
        if isinstance(day_name, str) and word in text_lower:
            target_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(day_name)
            current_day = today.weekday()
            days_ahead = (target_day - current_day) % 7
            if days_ahead == 0:
                days_ahead = 7  # Next week
            return today + timedelta(days=days_ahead)
    
    # Check for specific dates (e.g., "25 dekabr", "25 декабря")
    date_pattern = r'(\d{1,2})\s*(' + '|'.join(list(UZBEK_MONTHS.keys()) + list(RUSSIAN_MONTHS.keys())) + ')'
    match = re.search(date_pattern, text_lower)
    if match:
        day = int(match.group(1))
        month_word = match.group(2)
        month = UZBEK_MONTHS.get(month_word) or RUSSIAN_MONTHS.get(month_word)
        if month and 1 <= day <= 31:
            year = today.year
            if month < today.month or (month == today.month and day < today.day):
                year += 1
            return datetime(year, month, day)
    
    return None

def is_note_intent(text: str) -> bool:
    """Determine if message is intended for notes"""
    text_lower = text.lower()
    
    # Check for explicit note keywords
    if any(keyword in text_lower for keyword in NOTE_KEYWORDS_UZ + NOTE_KEYWORDS_RU):
        return True
    
    # Check for absence of time indicators (suggests it's a note, not event)
    has_time = parse_time(text) is not None
    has_date = parse_date(text) is not None
    
    # If no time/date, likely a note
    if not has_time and not has_date:
        # But check if it's a shopping list or task
        task_indicators = ['olish', 'sotib', 'купить', 'сделать', 'список']
        if any(indicator in text_lower for indicator in task_indicators):
            return True
    
    return False

def parse_uzbek_russian_message(text: str) -> Optional[Dict]:
    """
    Parse Uzbek/Russian message and determine intent
    Returns dict with intent, title, datetime, etc.
    """
    if not text or len(text.strip()) == 0:
        return None
    
    text = text.strip()
    
    # Determine if it's a note or calendar event
    is_note = is_note_intent(text)
    
    if is_note:
        # Extract note title and content
        # Remove note keywords
        cleaned = text
        for keyword in NOTE_KEYWORDS_UZ + NOTE_KEYWORDS_RU:
            cleaned = re.sub(rf'\b{keyword}\b:?\s*', '', cleaned, flags=re.IGNORECASE)
        
        return {
            'intent': 'note',
            'title': cleaned[:100],  # First 100 chars as title
            'content': cleaned
        }
    
    else:
        # Calendar event
        date = parse_date(text)
        time = parse_time(text)
        
        if not date and not time:
            # No date/time found, treat as note
            return {
                'intent': 'note',
                'title': text[:100],
                'content': text
            }
        
        # Use today if no date specified
        if not date:
            date = datetime.now()
        
        # Use default time if not specified
        if not time:
            time = "09:00"
        
        # Combine date and time
        hour, minute = map(int, time.split(':'))
        event_datetime = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Extract title (remove date/time words)
        title = text
        # Remove common time/date phrases
        remove_patterns = [
            r'(?:soat|в|kuni)\s*\d{1,2}(?::\d{2})?',
            r'\d{1,2}:\d{2}',
            r'\d{1,2}\.\d{2}',
            r'\b(' + '|'.join(list(UZBEK_DAYS.keys()) + list(RUSSIAN_DAYS.keys())) + r')\b',
            r'\d{1,2}\s*(' + '|'.join(list(UZBEK_MONTHS.keys()) + list(RUSSIAN_MONTHS.keys())) + r')',
            r'\bda\b', r'\bв\b', r'\bna\b'
        ]
        
        for pattern in remove_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        title = re.sub(r'\s+', ' ', title).strip()
        
        if not title:
            title = "Voqea / Событие"
        
        return {
            'intent': 'calendar',
            'title': title,
            'datetime': event_datetime.isoformat(),
            'description': text
        }

# Test function
if __name__ == '__main__':
    test_messages = [
        "Ertaga soat 14:00 da doktor",
        "Завтра в 15:30 встреча",
        "Non va sut sotib olish",
        "Eslatma: kitob o'qish",
        "Dushanba kuni 10 da yig'ilish",
        "25 dekabr soat 18:00 da bozor"
    ]
    
    for msg in test_messages:
        result = parse_uzbek_russian_message(msg)
        print(f"\n'{msg}'")
        print(f"Result: {result}")