#!/usr/bin/env python3
"""
Test script to verify NamedTuple usage patterns and Python 3.13 compatibility
"""

from typing import NamedTuple
from collections import namedtuple
import sys

print(f"Python version: {sys.version}")
print("="*60)

# Test 1: Class-based NamedTuple (recommended)
print("\n1. Testing class-based NamedTuple...")
try:
    class TestRecord1(NamedTuple):
        url: str
        name: str
        description: str
    
    record1 = TestRecord1(url="https://example.com", name="Test", description="Sample")
    print(f"   ✓ Class-based NamedTuple works: {record1}")
except Exception as e:
    print(f"   ✗ Class-based NamedTuple failed: {e}")

# Test 2: Functional style with list of tuples
print("\n2. Testing functional NamedTuple with list...")
try:
    TestRecord2 = NamedTuple('TestRecord2', [
        ('url', str),
        ('name', str),
        ('description', str)
    ])
    record2 = TestRecord2(url="https://example.com", name="Test", description="Sample")
    print(f"   ✓ Functional NamedTuple (list) works: {record2}")
except Exception as e:
    print(f"   ✗ Functional NamedTuple (list) failed: {e}")

# Test 3: collections.namedtuple (old style)
print("\n3. Testing collections.namedtuple...")
try:
    TestRecord3 = namedtuple('TestRecord3', ['url', 'name', 'description'])
    record3 = TestRecord3(url="https://example.com", name="Test", description="Sample")
    print(f"   ✓ collections.namedtuple works: {record3}")
except Exception as e:
    print(f"   ✗ collections.namedtuple failed: {e}")

# Test 4: Potential issue - using dict (WRONG - will fail)
print("\n4. Testing incorrect dict syntax (should fail)...")
try:
    TestRecord4 = NamedTuple('TestRecord4', {
        'url': str,
        'name': str,
        'description': str
    })
    record4 = TestRecord4(url="https://example.com", name="Test", description="Sample")
    print(f"   ✗ Dict syntax should have failed but didn't: {record4}")
except Exception as e:
    print(f"   ✓ Dict syntax correctly failed: {type(e).__name__}: {e}")

# Test 5: Test with capitalized field name "Url" specifically
print("\n5. Testing with capitalized 'Url' field...")
try:
    class TestRecord5(NamedTuple):
        Url: str
        Name: str
    
    record5 = TestRecord5(Url="https://example.com", Name="Test")
    print(f"   ✓ Capitalized field names work: {record5}")
except Exception as e:
    print(f"   ✗ Capitalized field names failed: {e}")

# Test 6: collections.namedtuple with string field names
print("\n6. Testing collections.namedtuple with string list...")
try:
    TestRecord6 = namedtuple('TestRecord6', 'url name description')
    record6 = TestRecord6(url="https://example.com", name="Test", description="Sample")
    print(f"   ✓ String field names work: {record6}")
except Exception as e:
    print(f"   ✗ String field names failed: {e}")

print("\n" + "="*60)
print("All NamedTuple tests completed!")
print("="*60)
