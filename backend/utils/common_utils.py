"""
Utility functions for the Store Opening AI system
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from flask import jsonify


def parse_iso_datetime(date_string: str) -> datetime:
    """
    Parse an ISO 8601 datetime string, handling timezone indicators
    
    Args:
        date_string: ISO 8601 formatted datetime string (e.g., "2024-05-15T00:00:00Z")
    
    Returns:
        datetime object
    
    Raises:
        ValueError: If the date string is not in valid ISO format
    """
    # Replace 'Z' with '+00:00' for timezone-aware parsing
    normalized_date = date_string.replace('Z', '+00:00')
    return datetime.fromisoformat(normalized_date)


def format_datetime(dt: Optional[datetime], format_string: str = '%Y-%m-%d %H:%M:%S') -> Optional[str]:
    """
    Format a datetime object to string
    
    Args:
        dt: datetime object to format (can be None)
        format_string: strftime format string
    
    Returns:
        Formatted datetime string, or None if dt is None
    """
    if dt is None:
        return None
    return dt.strftime(format_string)


def format_phone_number(phone: str) -> str:
    """
    Format phone number to E.164 format for Twilio
    
    Args:
        phone: Phone number in any format
    
    Returns:
        Phone number in E.164 format (e.g., "+1234567890")
    """
    # Remove common formatting characters
    cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Add + if not present
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    return cleaned


def calculate_days_between(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate number of days between two dates
    
    Args:
        start_date: Start datetime
        end_date: End datetime
    
    Returns:
        Number of days (can be negative if end_date is before start_date)
    """
    delta = end_date - start_date
    return delta.days


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Optional[tuple]:
    """
    Validate that all required fields are present in the data
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    
    Returns:
        None if validation passes, or (error_response, status_code) tuple if validation fails
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        error_message = f"Missing required field(s): {', '.join(missing_fields)}"
        return jsonify({'error': error_message}), 400
    
    return None
