# Saas-Backend

A multi-tenant SaaS Backend built with FastAPI, PostgreSQL, and Docker.

## Features
- REST API with FastAPI
- Pydantic data validation with email validation
- Modular router structure
- Proper HTTP error handling (404, 400, 422)
- Separate schemas file

## Coming Soon
- PostgreSQL + SQLAlchemy
- JWT Authentication
- Role-Based Access Control (RBAC)
- Multi-tenant architecture
- Docker + Deployment
- Redis caching

## Tech Stack
- Python 3.12
- FastAPI
- Pydantic v2
- uvicorn

## Project Structure
```
SaaS-Backend/
├── main.py
├── schemas.py
├── routers/
│   └── users.py
├── requirements.txt
└── .gitignore
```

## Setup
```bash
git clone https://github.com/saksham-42/Saas-Backend.git
cd Saas-Backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Welcome message |
| GET | /health | Server status |
| GET | /users/ | Get all users |
| GET | /users/{id} | Get one user |
| POST | /users/{id} | Create user |
| PUT | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user |

## Status
Week 1 — FastAPI Core Complete
Week 2 — PostgreSQL (In progress)