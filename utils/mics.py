from datetime import date, datetime, timedelta

def next_update_day() -> date:
    return datetime.now().date() + timedelta(days=1)