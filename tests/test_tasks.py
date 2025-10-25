"""
Tests para endpoints de tareas
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Variables globales para los tests
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
}

access_token = None

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup antes de cada test"""
    global access_token
    
    # Registrar usuario de prueba
    response = client.post("/api/auth/register", json=test_user)
    
    # Login y obtener token
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]}
    )
    access_token = login_response.json()["access_token"]
    
    yield
    
    # Cleanup después de cada test si es necesario

def get_auth_header():
    """Helper para obtener headers de autenticación"""
    return {"Authorization": f"Bearer {access_token}"}

def test_create_task():
    """Test crear una tarea"""
    task_data = {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea de prueba",
        "priority": 3
    }
    
    response = client.post(
        "/api/tasks/",
        json=task_data,
        headers=get_auth_header()
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data
    assert "created_at" in data

def test_get_all_tasks():
    """Test obtener todas las tareas"""
    # Crear algunas tareas primero
    for i in range(3):
        client.post(
            "/api/tasks/",
            json={"title": f"Tarea {i}", "priority": i+1},
            headers=get_auth_header()
        )
    
    response = client.get("/api/tasks/", headers=get_auth_header())
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

def test_get_task_by_id():
    """Test obtener una tarea específica"""
    # Crear una tarea
    create_response = client.post(
        "/api/tasks/",
        json={"title": "Tarea específica", "priority": 2},
        headers=get_auth_header()
    )
    task_id = create_response.json()["id"]
    
    # Obtener la tarea
    response = client.get(f"/api/tasks/{task_id}", headers=get_auth_header())
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Tarea específica"

def test_update_task():
    """Test actualizar una tarea"""
    # Crear una tarea
    create_response = client.post(
        "/api/tasks/",
        json={"title": "Tarea original", "priority": 1},
        headers=get_auth_header()
    )
    task_id = create_response.json()["id"]
    
    # Actualizar la tarea
    update_data = {
        "title": "Tarea actualizada",
        "status": "in_progress",
        "priority": 5
    }
    response = client.put(
        f"/api/tasks/{task_id}",
        json=update_data,
        headers=get_auth_header()
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["priority"] == update_data["priority"]

def test_delete_task():
    """Test eliminar una tarea"""
    # Crear una tarea
    create_response = client.post(
        "/api/tasks/",
        json={"title": "Tarea a eliminar", "priority": 1},
        headers=get_auth_header()
    )
    task_id = create_response.json()["id"]
    
    # Eliminar la tarea
    response = client.delete(f"/api/tasks/{task_id}", headers=get_auth_header())
    
    assert response.status_code == 204
    
    # Verificar que ya no existe
    get_response = client.get(f"/api/tasks/{task_id}", headers=get_auth_header())
    assert get_response.status_code == 404

def test_task_not_found():
    """Test obtener una tarea que no existe"""
    response = client.get("/api/tasks/99999", headers=get_auth_header())
    assert response.status_code == 404

def test_create_task_without_auth():
    """Test crear tarea sin autenticación debe fallar"""
    task_data = {"title": "Tarea sin auth", "priority": 1}
    response = client.post("/api/tasks/", json=task_data)
    assert response.status_code == 401

def test_task_validation():
    """Test validación de datos de tarea"""
    # Título vacío
    response = client.post(
        "/api/tasks/",
        json={"title": "", "priority": 1},
        headers=get_auth_header()
    )
    assert response.status_code == 422
    
    # Prioridad fuera de rango
    response = client.post(
        "/api/tasks/",
        json={"title": "Tarea", "priority": 10},
        headers=get_auth_header()
    )
    assert response.status_code == 422