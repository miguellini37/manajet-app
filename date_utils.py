"""
Date/Time Utility Functions for Manajet
Centralized date parsing and formatting to avoid duplication
"""

from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Parse datetime from various formats
    Returns datetime object or None if parsing fails

    Supported formats:
    - YYYY-MM-DD HH:MM:SS
    - YYYY-MM-DD HH:MM
    - YYYY-MM-DD
    - MM/DD/YYYY HH:MM
    - MM/DD/YYYY
    - DD/MM/YYYY HH:MM
    - DD/MM/YYYY
    """
    if not date_string:
        return None

    # Strip whitespace
    date_string = date_string.strip()

    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%m/%d/%Y %H:%M',
        '%m/%d/%Y',
        '%d/%m/%Y %H:%M',
        '%d/%m/%Y',
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    # If all formats fail, log warning
    logger.warning(f"Failed to parse date string: {date_string}")
    return None


def format_datetime(dt: datetime, include_time: bool = True) -> str:
    """
    Format datetime object to standard string format

    Args:
        dt: datetime object to format
        include_time: if True, includes time; if False, date only

    Returns:
        Formatted string (YYYY-MM-DD HH:MM or YYYY-MM-DD)
    """
    if not dt:
        return ""

    if include_time:
        return dt.strftime('%Y-%m-%d %H:%M')
    else:
        return dt.strftime('%Y-%m-%d')


def is_past(date_string: str) -> bool:
    """
    Check if a date/time is in the past

    Args:
        date_string: date string to check

    Returns:
        True if date is in the past, False otherwise
    """
    dt = parse_datetime(date_string)
    if not dt:
        return False

    return dt < datetime.now()


def is_future(date_string: str) -> bool:
    """
    Check if a date/time is in the future

    Args:
        date_string: date string to check

    Returns:
        True if date is in the future, False otherwise
    """
    dt = parse_datetime(date_string)
    if not dt:
        return False

    return dt > datetime.now()


def is_between(date_string: str, start_string: str, end_string: str) -> bool:
    """
    Check if a date is between two other dates

    Args:
        date_string: date to check
        start_string: start of range
        end_string: end of range

    Returns:
        True if date is between start and end (inclusive)
    """
    dt = parse_datetime(date_string)
    start = parse_datetime(start_string)
    end = parse_datetime(end_string)

    if not all([dt, start, end]):
        return False

    return start <= dt <= end


def days_until(date_string: str) -> Optional[int]:
    """
    Calculate days until a future date

    Args:
        date_string: future date to calculate

    Returns:
        Number of days (can be negative if in past), or None if invalid
    """
    dt = parse_datetime(date_string)
    if not dt:
        return None

    delta = dt - datetime.now()
    return delta.days


def hours_until(date_string: str) -> Optional[float]:
    """
    Calculate hours until a future datetime

    Args:
        date_string: future datetime to calculate

    Returns:
        Number of hours (can be negative if in past), or None if invalid
    """
    dt = parse_datetime(date_string)
    if not dt:
        return None

    delta = dt - datetime.now()
    return delta.total_seconds() / 3600
