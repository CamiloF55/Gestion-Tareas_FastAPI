from typing import List, Optional
from datetime import datetime
from models.task import Task, TaskCreate, TaskUpdate

class TaskService:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        task_dict = task_data.model_dump()
        task_dict.update({
            "id": self.next_id,
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
        
        task = Task(**task_dict)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_user_tasks(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        user_tasks = [task for task in self.tasks if task.user_id == user_id]
        return user_tasks[skip:skip + limit]
    
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        task = self.get_task_by_id(task_id)
        if task is None:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        task.updated_at = datetime.now()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

        # Crear instancia global compartida
task_service_instance = TaskService()