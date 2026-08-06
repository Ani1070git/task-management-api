# Task Management REST API

A production-ready REST API for managing tasks with user authentication and AI-powered task creation.

## Live Demo
**API:** https://task-management-api-production-09ab.up.railway.app  
**Documentation:** https://task-management-api-production-09ab.up.railway.app/docs

## Tech Stack

- **Python** - Core language
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Passlib + Bcrypt** - Password hashing
- **Groq + LLaMA** - AI task extraction
- **Docker** - Containerization
- **Railway** - Deployment

## Features

- User registration and login
- JWT token authentication
- Protected API endpoints
- Full CRUD operations for tasks
- AI-powered natural language task creation
- Persistent data storage with PostgreSQL
- Proper error handling with HTTP status codes
- Dockerized for easy deployment

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Register a new user |
| POST | /login | Login and get JWT token |

### Tasks (Protected - requires JWT token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a specific task |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| POST | /tasks/ai | Create task from natural language |

## AI Feature
Send a natural language message and the AI extracts the task title automatically.

Example:
```json
{"message": "Remind me to call my dentist tomorrow"}
```
Returns:
```json
{"id": 1, "title": "Call my dentist tomorrow", "done": false}
```

## Running Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up PostgreSQL and create a `.env` file
5. Start the server: `uvicorn main:app --reload`

## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/task_manager
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```