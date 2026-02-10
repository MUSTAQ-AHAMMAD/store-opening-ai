#!/usr/bin/env python3
"""
Verification script to test NamedTuple implementations
This script validates that the typing utilities work correctly
and demonstrates the fix for the NamedTuple error.
"""

import sys
from typing import NamedTuple

def test_incorrect_syntax():
    """Test that incorrect dict syntax fails as expected"""
    print("1. Testing incorrect dict syntax (should fail)...")
    try:
        # This is the WRONG way that causes the error in the problem statement
        TestRecord = NamedTuple('TestRecord', {
            'Url': str,
            'Name': str,
            'Description': str
        })
        print("   ✗ UNEXPECTED: Dict syntax should have failed!")
        return False
    except ValueError as e:
        print(f"   ✓ Correctly failed with: {e}")
        return True
    except Exception as e:
        print(f"   ✗ Failed with unexpected error: {e}")
        return False

def test_correct_class_syntax():
    """Test correct class-based syntax"""
    print("\n2. Testing correct class-based syntax...")
    try:
        class TestRecord(NamedTuple):
            Url: str
            Name: str
            Description: str
        
        record = TestRecord(
            Url="https://example.com",
            Name="Test",
            Description="Sample"
        )
        print(f"   ✓ Created successfully: {record}")
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_correct_functional_syntax():
    """Test correct functional syntax with list"""
    print("\n3. Testing correct functional syntax with list...")
    try:
        TestRecord = NamedTuple('TestRecord', [
            ('Url', str),
            ('Name', str),
            ('Description', str)
        ])
        
        record = TestRecord(
            Url="https://example.com",
            Name="Test",
            Description="Sample"
        )
        print(f"   ✓ Created successfully: {record}")
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_typing_utils():
    """Test the typing_utils module"""
    print("\n4. Testing typing_utils module...")
    try:
        from backend.utils.typing_utils import (
            StoreInfo, TaskSummary, TeamMemberInfo,
            create_dynamic_record
        )
        from datetime import datetime
        
        # Test predefined NamedTuples
        store = StoreInfo(1, "Test Store", "Location", "planning", datetime.now())
        task = TaskSummary(1, "Test Task", "pending", "high", "John")
        member = TeamMemberInfo(1, "Jane", "Manager", "+1234567890", "jane@example.com")
        
        print(f"   ✓ StoreInfo: {store.name}")
        print(f"   ✓ TaskSummary: {task.title}")
        print(f"   ✓ TeamMemberInfo: {member.name}")
        
        # Test dynamic creation
        DynamicRecord = create_dynamic_record('DynamicRecord', [
            ('url', str),
            ('count', int)
        ])
        dynamic = DynamicRecord(url="https://test.com", count=42)
        print(f"   ✓ DynamicRecord: {dynamic}")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("NamedTuple Implementation Verification")
    print("="*60)
    
    results = [
        test_incorrect_syntax(),
        test_correct_class_syntax(),
        test_correct_functional_syntax(),
        test_typing_utils()
    ]
    
    print("\n" + "="*60)
    if all(results):
        print("✓ All tests passed!")
        print("="*60)
        return 0
    else:
        print("✗ Some tests failed")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
