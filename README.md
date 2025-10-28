# Task Management API 📝

API RESTful para gestión de tareas construida con FastAPI, implementando arquitectura MVC y autenticación JWT.

## 🚀 Características

- ✅ CRUD completo de tareas
- 🔐 Autenticación JWT
- 👤 Gestión de usuarios
- 📊 Validación de datos con Pydantic
- 🏗️ Arquitectura MVC clara
- 📝 Documentación automática con Swagger
- 🧪 Tests unitarios y de integración
- 🔄 CI/CD configurado

![CI/CD Pipeline](https://github.com/CamiloF55/Gestion-Tareas_FastAPI/workflows/CI%2FCD%20Pipeline/badge.svg)

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd task-management-api
```

### 2. Crear entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Ejecución

### Modo desarrollo

```bash
python main.py
```

O con uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

### Documentación interactiva

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 Endpoints de la API

### Autenticación

#### Registrar usuario
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "usuario123",
  "email": "usuario@example.com",
  "password": "password123",
  "full_name": "Nombre Completo"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=usuario123&password=password123
```

#### Login (JSON)
```http
POST /api/auth/login/json
Content-Type: application/json

{
  "username": "usuario123",
  "password": "password123"
}
```

#### Obtener usuario actual
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Tareas (requieren autenticación)

#### Crear tarea
```http
POST /api/tasks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Mi tarea",
  "description": "Descripción de la tarea",
  "status": "pending",
  "priority": 3
}
```

#### Obtener todas las tareas
```http
GET /api/tasks/
Authorization: Bearer <token>
```

#### Obtener tarea por ID
```http
GET /api/tasks/{task_id}
Authorization: Bearer <token>
```

#### Actualizar tarea
```http
PUT /api/tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Tarea actualizada",
  "status": "completed",
  "priority": 5
}
```

#### Eliminar tarea
```http
DELETE /api/tasks/{task_id}
Authorization: Bearer <token>
```

## 🧪 Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=. --cov-report=html

# Ejecutar tests específicos
pytest tests/test_tasks.py
pytest tests/test_auth.py
```

## 🏗️ Arquitectura

### Patrón MVC

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Controllers       │  ← Maneja peticiones HTTP
│  (task_controller,  │
│   auth_controller)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│    Services         │  ← Lógica de negocio
│  (task_service,     │
│   auth_service)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│     Models          │  ← Estructura de datos
│  (task, user)       │
└─────────────────────┘
```

### Estructura de Directorios

```
task-management-api/
├── main.py                 # Punto de entrada
├── controllers/            # Controladores (C)
│   ├── task_controller.py
│   └── auth_controller.py
├── services/              # Lógica de negocio
│   ├── task_service.py
│   └── auth_service.py
├── models/                # Modelos de datos (M)
│   ├── task.py
│   └── user.py
├── middleware/            # Middleware
│   └── auth.py
└── tests/                 # Tests
    ├── test_tasks.py
    └── test_auth.py
```

## 🔒 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Hash de contraseñas**: Usando bcrypt
- **Validación de datos**: Automática con Pydantic
- **CORS**: Configurado para desarrollo
- **Manejo de errores**: Centralizado y seguro

## 📊 Estados de Tareas

- `pending`: Pendiente
- `in_progress`: En progreso
- `completed`: Completada

## 🎯 Prioridades

Las tareas tienen prioridad del 1 al 5:
- 1: Muy baja
- 2: Baja
- 3: Media
- 4: Alta
- 5: Muy alta

## 🔄 CI/CD

El proyecto incluye configuración para GitHub Actions que ejecuta:
- ✅ Tests automáticos
- 📊 Análisis de calidad de código
- 🚀 Despliegue automático (configurar según necesidad)

## 📝 Notas Importantes

⚠️ **IMPORTANTE**: Esta implementación usa almacenamiento en memoria. Los datos se pierden al reiniciar la aplicación. Para producción, se debe integrar una base de datos real (PostgreSQL, MySQL, MongoDB, etc.).

⚠️ **SEGURIDAD**: La SECRET_KEY en `auth_service.py` debe cambiarse en producción y almacenarse en variables de entorno.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Proyecto desarrollado como actividad académica de Servicios Web y CI/CD.

## 📞 Soporte

Para preguntas o problemas, abre un issue en el repositorio.