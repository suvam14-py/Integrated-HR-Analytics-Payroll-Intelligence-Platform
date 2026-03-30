import hashlib
import json
import os
from pathlib import Path
from datetime import datetime

class AuthManager:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Create users file with default admin account if it doesn't exist"""
        if not os.path.exists(self.users_file):
            os.makedirs('data', exist_ok=True)
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "name": "Administrator",
                    "role": "Admin",
                    "email": "admin@hranalytics.com",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "hr_manager": {
                    "password": self.hash_password("hr123"),
                    "name": "HR Manager",
                    "role": "HR Manager",
                    "email": "hr@hranalytics.com",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "analyst": {
                    "password": self.hash_password("analyst123"),
                    "name": "Data Analyst",
                    "role": "Analyst",
                    "email": "analyst@hranalytics.com",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Load users from JSON file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def verify_credentials(self, username, password):
        """Verify username and password"""
        users = self.load_users()
        
        if username in users:
            hashed_password = self.hash_password(password)
            if users[username]['password'] == hashed_password:
                return True, users[username]
        return False, None
    
    def create_user(self, username, password, name, role, email):
        """Create a new user account"""
        users = self.load_users()
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists"
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email') == email:
                return False, "Email already registered"
        
        # Create new user
        users[username] = {
            "password": self.hash_password(password),
            "name": name,
            "role": role,
            "email": email,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_users(users)
        return True, "Account created successfully"
    
    def reset_password(self, username, email, new_password):
        """Reset user password using email verification"""
        users = self.load_users()
        
        # Verify username exists
        if username not in users:
            return False, "Username not found"
        
        # Verify email matches
        if users[username]['email'] != email:
            return False, "Email does not match our records"
        
        # Update password
        users[username]['password'] = self.hash_password(new_password)
        users[username]['password_reset_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_users(users)
        return True, "Password reset successfully"
    
    def get_user_info(self, username):
        """Get user information"""
        users = self.load_users()
        return users.get(username, None)