"""
E-commerce API Module
=====================

Sample code for test generation.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

class UserService:
    def __init__(self):
        self.users = {}
    
    def create_user(self, user: User) -> User:
        if user.id in self.users:
            raise ValueError("User already exists")
        self.users[user.id] = user
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

@app.post("/users/")
def create_user(user: User):
    service = UserService()
    return service.create_user(user)

@app.get("/users/{user_id}")
def get_user(user_id: int):
    service = UserService()
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    service = UserService()
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Deleted"}
