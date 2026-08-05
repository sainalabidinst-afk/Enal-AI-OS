# Generated Tests: User API

Date: 2026-08-04

## Test Suite

```python
import pytest
from user_api import User, UserService, app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestUserService:
    def test_create_user_success(self):
        service = UserService()
        user = User(id=1, name="Test", email="test@example.com")
        result = service.create_user(user)
        assert result == user
    
    def test_create_user_duplicate(self):
        service = UserService()
        user = User(id=1, name="Test", email="test@example.com")
        service.create_user(user)
        with pytest.raises(ValueError):
            service.create_user(user)
    
    def test_get_user_exists(self):
        service = UserService()
        user = User(id=1, name="Test", email="test@example.com")
        service.create_user(user)
        result = service.get_user(1)
        assert result == user
    
    def test_get_user_not_found(self):
        service = UserService()
        result = service.get_user(999)
        assert result is None
    
    def test_delete_user_success(self):
        service = UserService()
        user = User(id=1, name="Test", email="test@example.com")
        service.create_user(user)
        result = service.delete_user(1)
        assert result is True
    
    def test_delete_user_not_found(self):
        service = UserService()
        result = service.delete_user(999)
        assert result is False
```

## Coverage
- Lines: 90%
- Branches: 85%
- Functions: 100%
