from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from services.task_service import TaskService
from middleware.auth import get_current_active_user

router = APIRouter()
from services.task_service import task_service_instance as task_service

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Crear una nueva tarea"""
    return task_service.create_task(task, current_user.id)

@router.get("/", response_model=List[Task])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todas las tareas del usuario actual"""
    return task_service.get_user_tasks(current_user.id, skip, limit)

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Obtener una tarea específica por su ID"""
    task = task_service.get_task_by_id(task_id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta tarea"
        )
    
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar una tarea existente"""
    task = task_service.get_task_by_id(task_id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta tarea"
        )
    
    return task_service.update_task(task_id, task_update)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar una tarea"""
    task = task_service.get_task_by_id(task_id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta tarea"
        )
    
    task_service.delete_task(task_id)
    return None