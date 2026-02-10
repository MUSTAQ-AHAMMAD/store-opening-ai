# Typing and NamedTuple Best Practices

## Overview
This document provides guidance on using type hints and NamedTuple in the Store Opening AI codebase, with special attention to Python 3.13+ compatibility.

## Common NamedTuple Error

### The Problem
When creating a NamedTuple using incorrect syntax, you may encounter this error:

```
File "typing.py", line 3106, in NamedTuple
    nt = _make_nmtuple(typename, fields, module=_caller())
File "typing.py", line 2983, in _make_nmtuple
    nm_tpl = collections.namedtuple(name, fields,
                                    defaults=defaults, module=module)
File "collections/__init__.py", line 444, in namedtuple
    __new__ = eval(code, namespace)
ValueError: too many values to unpack (expected 2)
```

### Root Cause
This error occurs when you try to pass a **dictionary** to `NamedTuple` instead of a **list of tuples**.

### ❌ INCORRECT Syntax (causes error)
```python
from typing import NamedTuple

# WRONG: Using dict syntax
MyRecord = NamedTuple('MyRecord', {
    'Url': str,
    'Name': str,
    'Description': str
})
```

### ✅ CORRECT Syntax

#### Option 1: Class-based (Recommended)
```python
from typing import NamedTuple

class MyRecord(NamedTuple):
    Url: str
    Name: str
    Description: str

# Usage
record = MyRecord(
    Url="https://example.com",
    Name="Example",
    Description="A sample record"
)
```

#### Option 2: Functional with List of Tuples
```python
from typing import NamedTuple

MyRecord = NamedTuple('MyRecord', [
    ('Url', str),
    ('Name', str),
    ('Description', str)
])

# Usage
record = MyRecord(
    Url="https://example.com",
    Name="Example",
    Description="A sample record"
)
```

#### Option 3: collections.namedtuple (Legacy)
```python
from collections import namedtuple

MyRecord = namedtuple('MyRecord', ['Url', 'Name', 'Description'])

# Usage
record = MyRecord(
    Url="https://example.com",
    Name="Example",
    Description="A sample record"
)
```

## Field Naming Rules

1. **Valid Identifiers**: Field names must be valid Python identifiers
   - Start with a letter (a-z, A-Z) or underscore (_)
   - Contain only letters, numbers, and underscores
   - Cannot start with a number

2. **Not Reserved Keywords**: Field names cannot be Python keywords
   - ❌ Bad: `class`, `if`, `for`, `def`, `return`
   - ✅ Good: `cls`, `if_value`, `for_loop`, `definition`, `result`

3. **Case Sensitivity**: Python is case-sensitive
   - `Url`, `url`, and `URL` are three different field names
   - Be consistent with your naming convention

## Python 3.13+ Compatibility

The class-based syntax is the most future-proof and compatible with all Python versions from 3.6 onwards:

```python
from typing import NamedTuple, Optional
from datetime import datetime

class StoreRecord(NamedTuple):
    """Store information with type hints"""
    id: int
    name: str
    location: str
    opening_date: Optional[datetime] = None
    status: str = "planning"

# This works in Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13+
```

## Best Practices

1. **Use Class-based Syntax**: It's more readable and maintainable
2. **Add Type Hints**: Always specify types for fields
3. **Use Optional**: For fields that can be None
4. **Set Defaults**: Use default values when appropriate
5. **Add Docstrings**: Document what the NamedTuple represents
6. **Import from typing**: Use `from typing import NamedTuple` not `from collections import namedtuple` for new code

## Using NamedTuples in This Project

See `backend/utils/typing_utils.py` for examples of properly defined NamedTuples used in this project:

- `StoreInfo`: Store information data transfer object
- `TaskSummary`: Task summary for reporting  
- `TeamMemberInfo`: Team member information

## Additional Resources

- [Python typing documentation](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
- [PEP 526 - Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
- [collections.namedtuple documentation](https://docs.python.org/3/library/collections.html#collections.namedtuple)

## Quick Reference

| Syntax | Python Version | Recommended | Type Hints |
|--------|----------------|-------------|------------|
| Class-based `typing.NamedTuple` | 3.6+ | ✅ Yes | ✅ Yes |
| Functional `typing.NamedTuple` | 3.5+ | ⚠️ Sometimes | ✅ Yes |
| `collections.namedtuple` | 2.6+ | ❌ Legacy only | ❌ No |
