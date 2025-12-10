"""
Form Helper Functions
Utilities for form validation and processing
"""

from flask import flash, redirect
from validators import sanitize_string
from typing import Dict, List, Tuple, Optional


def validate_and_flash(validations: List[Tuple[bool, Optional[str]]], redirect_url: str = None):
    """
    Validate multiple fields and flash first error

    Args:
        validations: List of (valid, error_message) tuples
        redirect_url: URL to redirect to if validation fails

    Returns:
        True if all valid, False otherwise (and flashes error)
    """
    for valid, error in validations:
        if not valid:
            flash(error, 'error')
            if redirect_url:
                return redirect(redirect_url)
            return False
    return True


def sanitize_form_dict(form_data: Dict[str, str], fields: List[str]) -> Dict[str, str]:
    """
    Sanitize multiple form fields

    Args:
        form_data: Request form data
        fields: List of field names to sanitize

    Returns:
        Dictionary of sanitized values
    """
    return {
        field: sanitize_string(form_data.get(field, ''))
        for field in fields
    }


def get_form_list(form_data: Dict[str, str], field_name: str) -> List[str]:
    """
    Get list of IDs from form data (for multi-select)

    Args:
        form_data: Request form data
        field_name: Name of the field

    Returns:
        List of selected IDs
    """
    return form_data.getlist(field_name) if hasattr(form_data, 'getlist') else []
