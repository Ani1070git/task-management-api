# Task Management REST API

A production-ready REST API for managing tasks with user authentication.

## Tech Stack

- **Python** - Core language
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Passlib + Bcrypt** - Password hashing

## Features

- User registration and login
- JWT token authentication
- Protected API endpoints
- Full CRUD operations for tasks
- Persistent data storage with PostgreSQL
- Proper error handling with HTTP status codes

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

## Running Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Set up PostgreSQL and create a `.env` file
5. Run `python init_db.py` to create tables
6. Start the server with `uvicorn main:app --reload`

## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/task_manager
```
