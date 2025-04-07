# 🧠 FastAPI + MongoDB REST API

Una API REST desarrollada con **FastAPI** y **MongoDB Atlas**, ideal para gestionar usuarios y tareas. Implementa validaciones con **Pydantic**, conexión segura vía `.env`, y una estructura modular ideal para expandir.

---

## 🚀 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) – Framework moderno para construir APIs
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) – Base de datos NoSQL en la nube
- [Pydantic](https://docs.pydantic.dev/) – Validación de datos en Python
- [Python-dotenv](https://pypi.org/project/python-dotenv/) – Gestión de variables de entorno

---

## 📬 Endpoints disponibles

### 👤 Usuarios

- **GET** `/get-users` → Obtener todos los usuarios
- **GET** `/get-user/{username}` → Obtener un usuario específico
- **POST** `/create-user` → Crear un nuevo usuario
- **PUT** `/update-user/{username}` → Actualizar datos de un usuario
- **DELETE** `/delete-user/{username}` → Eliminar un usuario

### ✅ Tareas

- **GET** `/get-tasks` → Obtener todas las tareas
- **GET** `/get-task/{title}` → Obtener una tarea por su título
- **POST** `/create-task` → Crear una nueva tarea
- **PUT** `/update-task/{title}` → Actualizar una tarea existente
- **DELETE** `/delete-task/{title}` → Eliminar una tarea


## ⚙️ Instalación

1. Cloná el repositorio


```bash
git clone https://github.com/juanifmera/fastapi-mongo-api.git
cd fastapi-mongo-api
