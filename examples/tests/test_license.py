#!/usr/bin/env python3
"""
Test script to demonstrate license verification
"""

import sys
import os

# Add current directory to path to import the obfuscator functions
sys.path.insert(0, os.path.dirname(__file__))

from simple_obfuscator import verify_license_key, get_machine_id

def test_license_verification():
    """Test license verification functionality"""

    print("🔍 Testing License Verification System")
    print("="*50)

    # Get current machine ID
    current_machine_id = get_machine_id()
    print(f"Current Machine ID: {current_machine_id}")

    # Test valid license (the one we generated)
    valid_license = "0a3a756bffd5fe563cb9b9ec3e5e17fb:1796752322:df5c55c1fb4969ac"
    print(f"\nTesting valid license: {valid_license}")
    is_valid, message = verify_license_key(valid_license)
    print(f"Result: {'✅ VALID' if is_valid else '❌ INVALID'} - {message}")

    # Test invalid license (wrong machine ID)
    invalid_license = "deadbeef1234567890abcdef123456:1796752322:df5c55c1fb4969ac"
    print(f"\nTesting invalid license (wrong machine): {invalid_license}")
    is_valid, message = verify_license_key(invalid_license)
    print(f"Result: {'✅ VALID' if is_valid else '❌ INVALID'} - {message}")

    # Test expired license (past timestamp)
    expired_license = f"{current_machine_id}:1609459200:df5c55c1fb4969ac"  # 2021 timestamp
    print(f"\nTesting expired license: {expired_license}")
    is_valid, message = verify_license_key(expired_license)
    print(f"Result: {'✅ VALID' if is_valid else '❌ INVALID'} - {message}")

    # Test malformed license
    malformed_license = "invalid-license-format"
    print(f"\nTesting malformed license: {malformed_license}")
    is_valid, message = verify_license_key(malformed_license)
    print(f"Result: {'✅ VALID' if is_valid else '❌ INVALID'} - {message}")

if __name__ == "__main__":
    test_license_verification()
