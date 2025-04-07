# Importación de librerías necesarias
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializamos la aplicación FastAPI
app = FastAPI()

# ---------- CONEXIÓN A MONGODB ----------
# URI de conexión a MongoDB Atlas
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    # Verificamos conexión con MongoDB
    client.admin.command('ping')
    print("Conectado exitosamente a MongoDB")

    # Accedemos a la base de datos y colecciones
    db = client['FastAPI']
    users_collection = db['users']
    tasks_collection = db['tasks']

    # Creamos índice único en username (case-insensitive)
    users_collection.create_index(
        [("username", 1)], unique=True, collation={"locale": "en", "strength": 2}
    )

except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")

# ---------- MODELOS Pydantic ----------

# Modelo para creación de usuario
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    full_name: str | None = None
    age: int = Field(default=18, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

# Modelo para actualización parcial de usuario
class UpdatedUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    full_name: str | None = None
    age: int | None = Field(default=18, ge=0)
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

# Modelo para tareas
class Task(BaseModel):
    title: str
    description: str | None = Field(default=None, max_length=50, min_length=5)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

# Modelo para actualización de tareas
class UpdatedTask(BaseModel):
    title: str
    description: str | None = Field(default=None, max_length=50, min_length=5)
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

# ---------- FUNCIONES DE SERIALIZACIÓN ----------

# Convierte ObjectId a string para JSON
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

def serialize_task(task):
    task["_id"] = str(task["_id"])
    return task

# ---------- ENDPOINTS DE USUARIOS ----------

# Obtener todos los usuarios
@app.get('/get-users', tags=['Users'])
async def get_all_users():
    users = list(users_collection.find({}))
    return {"users": [serialize_user(user) for user in users]}

# Obtener un usuario por su username
@app.get('/get-user/{username}', tags=['Users'])
async def get_by_username(username: str):
    user = users_collection.find_one({'username': username})
    if user:
        return {"User Found": serialize_user(user)}
    raise HTTPException(status_code=404, detail="User not found")

# Crear un nuevo usuario
@app.post('/create-user', tags=['Users'])
async def create_user(user: User):
    try:
        users_collection.insert_one(user.model_dump())
        return {"message": "User created successfully", 'user': f'{user.model_dump()}'}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username already exists")

# Eliminar un usuario por su username
@app.delete('/delete-user/{username}', tags=['Users'])
async def delete_user(username: str):
    search = users_collection.delete_one({'username': username})
    if search.deleted_count > 0:
        return {'Message': f'User {username} has been deleted successfully'}
    else:
        return {'Message': 'No username found in Data Base'}

# Actualizar datos de un usuario
@app.put('/update-user/{username}', tags=['Users'])
async def update_user(username: str, user: UpdatedUser):
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    search = users_collection.update_one({'username': username}, {'$set': update_data})

    if search.matched_count > 0:
        return {'Message': f'{user.username} has been modified successfully'}
    else:
        raise HTTPException(status_code=404, detail="No username found in Data Base")

# ---------- ENDPOINTS DE TAREAS ----------

# Obtener todas las tareas
@app.get('/get-tasks', tags=['Tasks'])
async def get_tasks():
    task_list = list(tasks_collection.find({}))
    if len(task_list) > 0:
        return {'Tasks': [serialize_task(task) for task in task_list]}
    else:
        return {'message': 'Error --> No tasks in collection'}

# Crear una nueva tarea
@app.post('/create-task', tags=['Tasks'])
async def create_task(task: Task):
    try:
        tasks_collection.insert_one(task.model_dump())  
        return {'Message': f'Task {task.title} created successfully'}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Task already exists")

# Obtener una tarea por su título
@app.get('/get-task/{task_title}', tags=['Tasks'])
async def get_task_by_title(task_title: str):
    tasks_list = list(tasks_collection.find({'title': task_title}))
    if len(tasks_list) > 0:
        return {'Message': [serialize_task(task) for task in tasks_list]}
    else:
        return {'Message': f'No tasks found with {task_title} title'}

# Actualizar una tarea por título
@app.put('/update-task/{task_title}', tags=['Tasks'])
async def update_task_by_id(task_title: str, task: UpdatedTask):
    update_task = {k: v for k, v in task.model_dump().items() if v is not None}

    if not update_task:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")
    
    search = tasks_collection.update_one({'title': task_title}, {'$set': update_task})

    if search.matched_count > 0:
        return {'Message': f'{task.title} has been modified successfully'}
    else:
        raise HTTPException(status_code=404, detail="No Task found in Data Base")

# Eliminar una tarea por título
@app.delete('/delete-task/{task_title}', tags=['Tasks'])
async def delete_task_by_title(task_title: str):
    search = tasks_collection.delete_one({'title': task_title})
    if search.deleted_count > 0:
        return {'message': f'Task {task_title} deleted successfully'}
    else:
        return {'message': 'Error no task found'}
