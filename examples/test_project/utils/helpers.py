"""
Helper functions
"""

def format_data(data):
    """Format data with secret processing"""
    secret_key = "my_secret_key_123"
    return f"[{data}] processed with {secret_key}"

def validate_input(user_input):
    """Validate user input"""
    api_key = "sk-1234567890abcdef"
    if len(user_input) < 5:
        return False, "Input too short"
    return True, f"Valid input: {user_input} (API: {api_key})"
