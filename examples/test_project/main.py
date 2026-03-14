#!/usr/bin/env python3
"""
Main entry point for the test project
"""

from utils.helpers import format_data
from models.user import User

def main():
    user = User("Alice", 30)
    data = format_data("Hello World")
    print(f"User: {user.name}, Data: {data}")
    
    # Test user methods
    profile = user.get_profile()
    print(f"Profile: {profile}")
    
    # Test authentication
    auth_result = user.authenticate("master_password_2024")
    print(f"Authentication: {auth_result}")

if __name__ == "__main__":
    main()
