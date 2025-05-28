# Lista de Tareas con FastAPI y React

Aplicación de lista de tareas (To-Do List) construida con FastAPI en el backend y React en el frontend, utilizando Redis como almacenamiento.

## Características

- **Backend (FastAPI)**:
  - API RESTful para gestionar tareas
  - Almacenamiento en Redis
  - Documentación automática con Swagger UI

- **Frontend (React)**:
  - Interfaz de usuario intuitiva y responsiva
  - Estado manejado con React Hooks
  - Diseño moderno y accesible

## Requisitos previos

- Python 3.8+
- Node.js 16+
- Redis
- npm o yarn

## Configuración del proyecto

### Backend

1. Crear un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno (opcional, crea un archivo `.env` en la carpeta backend):
   ```
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ```

4. Ejecutar el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```

El servidor estará disponible en `http://localhost:8000`

### Frontend

1. Instalar dependencias:
   ```bash
   cd frontend
   npm install
   ```

2. Configurar la URL de la API (opcional, modificar en `src/App.js`):
   ```javascript
   const API_URL = 'http://localhost:8000';
   ```

3. Ejecutar la aplicación en modo desarrollo:
   ```bash
   npm start
   ```

La aplicación estará disponible en `http://localhost:3000`

## Despliegue

### Backend (Northflank)

1. Crear un nuevo proyecto en Northflank
2. Agregar un servicio de Redis
3. Configurar las variables de entorno para conectar con Redis
4. Desplegar el código del backend

### Frontend (Vercel)

1. Conectar tu repositorio de GitHub con Vercel
2. Configurar el directorio de construcción como `frontend`
3. Establecer el comando de construcción: `npm run build`
4. Configurar la variable de entorno `REACT_APP_API_URL` con la URL de tu API desplegada

## Estructura del proyecto

```
.
├── backend/               # Código del servidor FastAPI
│   ├── main.py            # Punto de entrada de la aplicación
│   └── requirements.txt   # Dependencias de Python
├── frontend/              # Aplicación React
│   ├── public/            # Archivos estáticos
│   └── src/               # Código fuente de React
└── README.md              # Este archivo
```

## API Endpoints

- `GET /tasks/` - Obtener todas las tareas
- `POST /tasks/` - Crear una nueva tarea
- `GET /tasks/{task_id}` - Obtener una tarea específica
- `PUT /tasks/{task_id}` - Actualizar una tarea
- `DELETE /tasks/{task_id}` - Eliminar una tarea

## Licencia

Este proyecto está bajo la Licencia MIT.
