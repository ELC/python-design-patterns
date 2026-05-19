from datetime import date, datetime


def format_date(value: datetime | date) -> str:
    return value.strftime("%Y-%m-%d")
