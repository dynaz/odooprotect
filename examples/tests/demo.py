
import base64
import sys

_STRINGS = ['c3VwZXJfc2VjcmV0X2tleV8xMjM0NQ==', 'QWNjZXNzIGdyYW50ZWQh', 'QWNjZXNzIGRlbmllZCE=']  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    return base64.b64decode(encrypted).decode()


def secret_function(password):
    _obf_0 = _decrypt_str('0')
    if password == _obf_0:
        return _decrypt_str('1')
    else:
        return _decrypt_str('2')
