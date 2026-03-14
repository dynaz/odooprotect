#!/usr/bin/env python3
"""
Demonstrate machine binding by testing what happens with wrong license
"""

import sys
import os

def simulate_different_machine():
    """Simulate running on a different machine by temporarily changing license"""

    # Create a fake bound file with wrong machine ID
    fake_license = "deadbeef1234567890abcdef123456:1796752322:df5c55c1fb4969ac"  # Wrong machine ID

    fake_code = '''
import base64
import sys

_STRINGS = ['c3VwZXJfc2VjcmV0X2tleV8xMjM0NQ==', 'QWNjZXNzIGdyYW50ZWQh', 'QWNjZXNzIGRlbmllZCE=']

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    return base64.b64decode(encrypted).decode()

# License verification with WRONG machine ID
_LICENSE_KEY = "deadbeef1234567890abcdef123456:1796752322:df5c55c1fb4969ac"

def _get_machine_id():
    """Generate machine identifier"""
    import hashlib
    import platform
    import uuid
    import subprocess

    components = []
    try:
        cpu_info = platform.processor()
        if cpu_info:
            components.append("cpu:" + cpu_info)
    except:
        pass

    try:
        machine = platform.machine()
        if machine:
            components.append("arch:" + machine)
    except:
        pass

    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2*6, 2)][::-1])
        components.append("mac:" + mac)
    except:
        pass

    try:
        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            disk_serial = result.stdout.strip().split('\n')[0]
            if disk_serial:
                components.append("disk:" + disk_serial)
    except:
        pass

    combined = '|'.join(components)
    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]
    return machine_id

def _verify_license_key(license_key):
    """Verify license validity"""
    import hashlib
    import time

    try:
        parts = license_key.split(':')
        if len(parts) != 3:
            return False

        machine_id = parts[0]
        expiration = int(parts[1])
        signature = parts[2]

        current_time = int(time.time())
        if current_time > expiration:
            return False

        expected_signature = hashlib.sha256(("secret_salt:" + machine_id + ":" + str(expiration)).encode()).hexdigest()[:16]
        if signature != expected_signature:
            return False

        current_machine_id = _get_machine_id()
        if machine_id != current_machine_id:
            return False

        return True
    except:
        return False

def _check_license():
    """Verify license on startup"""
    if not _verify_license_key(_LICENSE_KEY):
        print("ERROR: Invalid or expired license!")
        print("This software is licensed to run on a different machine.")
        import sys
        sys.exit(1)

# Obfuscated code
def secret_function(password):
    _obf_0 = _decrypt_str('0')
    if password == _obf_0:
        return _decrypt_str('1')
    else:
        return _decrypt_str('2')

# Check license at the end
_check_license()
'''

    print("🚫 Testing machine binding with WRONG license key...")
    print("This simulates running the bound code on a different machine.")
    print()

    try:
        exec(fake_code)
        print("❌ ERROR: Code should have been blocked!")
    except SystemExit as e:
        print("✅ SUCCESS: Code was properly blocked by license verification!")
        print(f"   Exit code: {e.code}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    simulate_different_machine()
