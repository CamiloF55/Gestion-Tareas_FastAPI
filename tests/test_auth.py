import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    """Test registrar un nuevo usuario"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123456",
        "full_name": "Test User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data

def test_login_success():
    """Test login exitoso"""
    # Primero registrar
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass123"
    }
    client.post("/api/auth/register", json=user_data)
    
    # Luego login
    response = client.post(
        "/api/auth/login",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test login con contraseña incorrecta"""
    user_data = {
        "username": "wrongpass",
        "email": "wrong@example.com",
        "password": "correctpass"
    }
    client.post("/api/auth/register", json=user_data)
    
    response = client.post(
        "/api/auth/login",
        data={"username": user_data["username"], "password": "wrongpassword"}
    )
    
    assert response.status_code == 401