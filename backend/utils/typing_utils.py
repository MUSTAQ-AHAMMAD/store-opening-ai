"""
Typing Utilities and Common Type Definitions
Provides type hints and NamedTuple definitions for the Store Opening AI system
"""

from typing import NamedTuple, Optional
from datetime import datetime


# Example NamedTuples for API responses and data transfer objects
# Using class-based syntax (recommended for Python 3.6+)

class StoreInfo(NamedTuple):
    """Store information data transfer object"""
    id: int
    name: str
    location: str
    status: str
    opening_date: Optional[datetime] = None


class TaskSummary(NamedTuple):
    """Task summary for reporting"""
    task_id: int
    title: str
    status: str
    priority: str
    assigned_to: Optional[str] = None


class TeamMemberInfo(NamedTuple):
    """
    Team member information
    
    Note: phone is required (not Optional) because it's used for WhatsApp integration
    and SMS notifications. Email is optional as it's not used for primary communication.
    This mirrors the database model where phone is NOT NULL and email is nullable.
    """
    id: int
    name: str
    role: str
    phone: str
    email: Optional[str] = None


# Example of correct functional NamedTuple syntax (if needed for dynamic creation)
# Use list of tuples: [('field_name', type), ...]
# NOT dict: {'field_name': type, ...}  <- This will cause "too many values to unpack" error

def create_dynamic_record(name: str, fields: list) -> type:
    """
    Create a NamedTuple dynamically with proper syntax
    
    Args:
        name: Name of the new NamedTuple class
        fields: List of (field_name, field_type) tuples
        
    Example:
        >>> RecordType = create_dynamic_record('RecordType', [
        ...     ('url', str),
        ...     ('name', str),
        ...     ('count', int)
        ... ])
        >>> record = RecordType(url='http://example.com', name='Test', count=5)
    
    Returns:
        A new NamedTuple class
    """
    return NamedTuple(name, fields)


# Best Practices for NamedTuple usage:
# 
# 1. RECOMMENDED: Use class-based syntax for static definitions
#    class MyRecord(NamedTuple):
#        field1: str
#        field2: int
#
# 2. For dynamic creation, use list of tuples:
#    MyRecord = NamedTuple('MyRecord', [('field1', str), ('field2', int)])
#
# 3. AVOID: Using dict syntax - this will fail!
#    MyRecord = NamedTuple('MyRecord', {'field1': str, 'field2': int})  # WRONG!
#
# 4. Field names must be valid Python identifiers
#    - Start with letter or underscore
#    - Contain only letters, numbers, underscores
#    - Cannot be Python keywords (if, for, class, etc.)
#
# 5. For Python 3.13+ compatibility, always use proper syntax
