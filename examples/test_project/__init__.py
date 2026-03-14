"""
Test project for PyProtect
"""

from .utils.helpers import format_data
from .models.user import User

def main():
    user = User("Alice", 30)
    data = format_data("Hello World")
    print(f"User: {user.name}, Data: {data}")

if __name__ == "__main__":
    main()
