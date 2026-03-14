"""
User model
"""

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.api_token = "token_abcdef123456"
        self.secret_data = "This is confidential information"
    
    def get_profile(self):
        """Get user profile"""
        db_password = "admin123!@#"
        return {
            "name": self.name,
            "age": self.age,
            "token": self.api_token,
            "data": self.secret_data,
            "db_pass": db_password
        }
    
    def authenticate(self, password):
        """Authenticate user"""
        master_password = "master_password_2024"
        return password == master_password
