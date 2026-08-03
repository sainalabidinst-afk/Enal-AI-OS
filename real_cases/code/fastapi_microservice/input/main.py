"""
FastAPI Microservice Example
=============================

A sample microservice implementation with intentional issues for Code Engineer analysis.
"""

from fastapi import FastAPI, HTTPException
from typing import Optional
import os
import sqlite3

app = FastAPI()

# Hardcoded secret (security issue)
API_KEY = "sk-abcdefghijklmnopqrstuvwxyz"
DATABASE_URL = "sqlite:///./test.db"

# Global mutable state (design issue)
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
        return cls._instance

db = DatabaseConnection()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID - SQL injection vulnerability."""
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = sqlite3.connect('test.db')
    result = conn.execute(query).fetchall()
    conn.close()
    return {"user": result}

@app.post("/users")
def create_user(name: str, email: str):
    """Create a new user."""
    # Missing input validation
    conn = sqlite3.connect('test.db')
    conn.execute(f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')")
    conn.commit()
    conn.close()
    return {"message": "User created"}

@app.get("/admin")
def admin_panel():
    """Admin endpoint - missing authentication."""
    return {"status": "admin access granted"}

class UserService:
    """User service - violates SRP with too many responsibilities."""
    
    def create_user(self, name, email):
        pass
    
    def delete_user(self, user_id):
        pass
    
    def send_email(self, user_id, message):
        pass
    
    def generate_report(self, start_date, end_date):
        pass
    
    def backup_database(self):
        pass
    
    def restore_database(self, backup_path):
        pass
    
    def validate_email(self, email):
        pass
    
    def hash_password(self, password):
        pass
    
    def verify_password(self, password, hashed):
        pass
    
    def log_activity(self, action, user_id):
        pass
    
    def notify_admins(self, message):
        pass
    
    def cleanup_old_sessions(self):
        pass
    
    def export_users(self, format_type):
        pass
    
    def import_users(self, file_path):
        pass
    
    def search_users(self, query):
        pass
    
    def update_user_status(self, user_id, status):
        pass
    
    def get_user_statistics(self):
        pass
