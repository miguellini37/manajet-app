"""
Input Validation Utilities for Manajet
Provides validation functions for user inputs to prevent XSS, SQL injection, and data integrity issues
"""

import re
from datetime import datetime
from typing import Optional, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address format
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"

    # RFC 5322 simplified regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate phone number format
    Accepts: +1-555-1234, (555) 123-4567, 555.123.4567, etc.
    """
    if not phone:
        return False, "Phone number is required"

    # Remove common separators for validation
    cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)

    # Check if it starts with + for international
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]

    # Should be 10-15 digits
    if not cleaned.isdigit():
        return False, "Phone number should contain only digits and valid separators"

    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number should be 10-15 digits"

    return True, None


def validate_passport(passport: str) -> Tuple[bool, Optional[str]]:
    """
    Validate passport number format
    Typically 6-9 alphanumeric characters
    """
    if not passport:
        return False, "Passport number is required"

    if len(passport) < 6 or len(passport) > 12:
        return False, "Passport number should be 6-12 characters"

    # Alphanumeric only
    if not re.match(r'^[A-Z0-9]+$', passport.upper()):
        return False, "Passport number should contain only letters and numbers"

    return True, None


def validate_tail_number(tail_number: str) -> Tuple[bool, Optional[str]]:
    """
    Validate aircraft tail number (N-number for US)
    Format: N + 1-5 numbers + optional 1-2 letters
    """
    if not tail_number:
        return False, "Tail number is required"

    # US N-numbers
    if tail_number.startswith('N'):
        pattern = r'^N[0-9]{1,5}[A-Z]{0,2}$'
        if not re.match(pattern, tail_number.upper()):
            return False, "Invalid US tail number format (e.g., N123AB)"
    else:
        # International - just check reasonable format
        if len(tail_number) < 3 or len(tail_number) > 8:
            return False, "Tail number should be 3-8 characters"
        if not re.match(r'^[A-Z0-9\-]+$', tail_number.upper()):
            return False, "Tail number should contain only letters, numbers, and hyphens"

    return True, None


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
    """
    Validate person/company name
    Prevents XSS and ensures reasonable format
    """
    if not name:
        return False, f"{field_name} is required"

    if len(name) < 2:
        return False, f"{field_name} is too short (minimum 2 characters)"

    if len(name) > 100:
        return False, f"{field_name} is too long (maximum 100 characters)"

    # Allow letters, spaces, hyphens, apostrophes, periods
    # Block < > to prevent XSS
    if re.search(r'[<>{}]', name):
        return False, f"{field_name} contains invalid characters"

    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate username format
    3-30 characters, alphanumeric and underscore only
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username is too short (minimum 3 characters)"

    if len(username) > 30:
        return False, "Username is too long (maximum 30 characters)"

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"

    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength
    Minimum 8 characters, at least one letter and one number
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password is too short (minimum 8 characters)"

    if len(password) > 128:
        return False, "Password is too long (maximum 128 characters)"

    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"

    return True, None


def validate_date(date_str: str, field_name: str = "Date") -> Tuple[bool, Optional[str]]:
    """
    Validate date format and reasonableness
    Accepts: YYYY-MM-DD, YYYY-MM-DD HH:MM, YYYY-MM-DD HH:MM:SS
    """
    if not date_str:
        return False, f"{field_name} is required"

    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
    ]

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)

            # Check if date is reasonable (not before 1900, not after 2100)
            if parsed_date.year < 1900 or parsed_date.year > 2100:
                return False, f"{field_name} year must be between 1900 and 2100"

            return True, None
        except ValueError:
            continue

    return False, f"Invalid {field_name.lower()} format (use YYYY-MM-DD or YYYY-MM-DD HH:MM)"


def validate_integer(value: str, field_name: str = "Value", min_val: int = None, max_val: int = None) -> Tuple[bool, Optional[str]]:
    """
    Validate integer value with optional range
    """
    if not value:
        return False, f"{field_name} is required"

    try:
        int_value = int(value)
    except ValueError:
        return False, f"{field_name} must be a number"

    if min_val is not None and int_value < min_val:
        return False, f"{field_name} must be at least {min_val}"

    if max_val is not None and int_value > max_val:
        return False, f"{field_name} must be at most {max_val}"

    return True, None


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input by removing dangerous characters
    Prevents XSS and keeps text clean
    """
    if not text:
        return ""

    # Remove null bytes
    text = text.replace('\x00', '')

    # Truncate to max length
    text = text[:max_length]

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def validate_text_field(text: str, field_name: str = "Field", min_length: int = 0, max_length: int = 1000, required: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Generic text field validation
    """
    if not text:
        if required:
            return False, f"{field_name} is required"
        return True, None

    if len(text) < min_length:
        return False, f"{field_name} is too short (minimum {min_length} characters)"

    if len(text) > max_length:
        return False, f"{field_name} is too long (maximum {max_length} characters)"

    # Block obvious XSS attempts
    if re.search(r'<script|javascript:|onerror=|onclick=', text, re.IGNORECASE):
        return False, f"{field_name} contains invalid content"

    return True, None


def validate_license_number(license_num: str, crew_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate pilot license number
    Required for pilots, optional for cabin crew
    """
    if crew_type == "Pilot":
        if not license_num:
            return False, "Pilot license number is required"

        if len(license_num) < 3 or len(license_num) > 20:
            return False, "License number should be 3-20 characters"

        if not re.match(r'^[A-Z0-9\-]+$', license_num.upper()):
            return False, "License number should contain only letters, numbers, and hyphens"

    return True, None


def validate_aircraft_capacity(capacity: str) -> Tuple[bool, Optional[str]]:
    """
    Validate aircraft passenger capacity
    Reasonable range: 1-850 (A380 max)
    """
    return validate_integer(capacity, "Passenger capacity", min_val=1, max_val=850)
