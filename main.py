"""
API RESTful para Gestión de Tareas
Arquitectura: MVC (Model-View-Controller)
Framework: FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.task_controller import router as task_router
from controllers.auth_controller import router as auth_router

app = FastAPI(
    title="Task Management API",
    description="API RESTful para gestión de tareas con autenticación JWT",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers (Controllers)
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(task_router, prefix="/api/tasks", tags=["Tareas"])

@app.get("/")
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)