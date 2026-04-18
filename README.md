# SaaS Backend

[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)](https://saas-backend-a4fl.onrender.com)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)

A production-grade multi-tenant SaaS Backend built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.

🌐 **Live URL:** https://saas-backend-a4fl.onrender.com  
📖 **API Docs:** https://saas-backend-a4fl.onrender.com/docs  
❤️ **Health Check:** https://saas-backend-a4fl.onrender.com/health

> ⚠️ Hosted on Render free tier — first request may take ~50 seconds to wake up.

---

## Features

- JWT Authentication with refresh token rotation
- Role-Based Access Control (RBAC) — admin/member roles per organization
- Multi-tenant architecture with strict data isolation
- Organization & membership system
- Task management with priority, due dates, assignment, and soft deletes
- Pagination on all list endpoints
- Connection pooling with SQLAlchemy
- Pydantic v2 validation with custom validators
- Centralized logging with request IDs and response times
- Request logging middleware
- Dockerized with docker-compose for local development
- Graceful shutdown with lifespan events
- Health check endpoint with real DB connection test

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | python-jose (JWT) + bcrypt |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Containerization | Docker + Docker Compose |
| Deployment | Render |
| Config | pydantic-settings |

---

## Architecture

```
Client
  │
  ▼
FastAPI (Uvicorn)
  │
  ├── Middleware (RequestLoggingMiddleware)
  │
  ├── Routers (HTTP layer only)
  │     ├── auth.py
  │     ├── users.py
  │     ├── organizations.py
  │     └── tasks.py
  │
  ├── Services (Business logic)
  │     ├── auth_service.py
  │     ├── user_service.py
  │     ├── org_service.py
  │     └── task_service.py
  │
  ├── CRUD (DB queries only)
  │     ├── users.py
  │     ├── organizations.py
  │     └── tasks.py
  │
  └── PostgreSQL (via SQLAlchemy)
```

---

## Project Structure

```
SaaS-Backend/
├── app/
│   ├── main.py                 # FastAPI app, lifespan events
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── hashing.py
│   │   └── tokens.py
│   ├── core/
│   │   ├── config.py           # pydantic-settings
│   │   ├── db.py               # engine, session, Base
│   │   ├── logging.py          # centralized logger
│   │   └── middleware.py       # request logging middleware
│   ├── crud/
│   │   ├── organizations.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── models/
│   │   ├── organization.py
│   │   ├── organization_member.py
│   │   ├── refresh_token.py
│   │   ├── task.py
│   │   └── user.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── organizations.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── schemas/
│   └── services/
│       ├── auth_service.py
│       ├── org_service.py
│       ├── task_service.py
│       └── user_service.py
├── alembic/
│   └── versions/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
└── alembic.ini
```

---

## Local Setup

### Without Docker

```bash
git clone https://github.com/saksham-42/Saas-Backend.git
cd SaaS-Backend
python -m venv env
env\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/saas_db
TEST_DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/saas_test
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EXPIRE_MINUTES=180
```

Run migrations:

```bash
alembic upgrade head
```

Start server:

```bash
uvicorn app.main:app --reload
```

### With Docker

```bash
docker compose up --build
```

This spins up the FastAPI app and PostgreSQL together. App available at `http://localhost:8000`.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `TEST_DATABASE_URL` | ❌ | Only needed for running tests locally |
| `SECRET_KEY` | ✅ | JWT signing key |
| `ALGORITHM` | ✅ | JWT algorithm (HS256) |
| `EXPIRE_MINUTES` | ✅ | Access token expiry in minutes |

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login, returns JWT |
| POST | /auth/refresh | Refresh access token |
| POST | /auth/logout | Revoke refresh token |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | /users/me | Get current logged-in user |
| GET | /users/ | List all users |
| GET | /users/{id} | Get user by ID |
| PUT | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user (admin only) |
| GET | /users/me/tasks | All tasks assigned to me |

### Organizations
| Method | Endpoint | Description |
|---|---|---|
| POST | /organization/ | Create organization |
| GET | /organization/{id} | Get organization |
| POST | /organization/{id}/members | Add member (admin only) |
| GET | /organization/{id}/members | List members |
| DELETE | /organization/{id}/members/{user_id} | Remove member (admin only) |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| POST | /organization/{id}/tasks | Create task |
| GET | /organization/{id}/tasks | List tasks |
| PUT | /organization/{id}/tasks/{task_id} | Update task |
| PATCH | /organization/{id}/tasks/{task_id}/assign | Assign task |
| DELETE | /organization/{id}/tasks/{task_id} | Soft delete task |

### System
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Root — service status |
| GET | /health | Health check with DB ping |

---

## Database Schema

### users
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| name | varchar | min 2 chars |
| email | varchar | unique, indexed |
| hashed_password | varchar | bcrypt |
| role | varchar | admin / member |

### organizations
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| name | varchar | |
| slug | varchar | unique |
| owner_id | int | FK → users |
| created_at | timestamp | |

### organization_members
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| org_id | int | FK → organizations |
| user_id | int | FK → users |
| role | varchar | admin / member |

### tasks
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| title | varchar | |
| description | varchar | nullable |
| status | varchar | pending / in_progress / completed |
| priority | varchar | low / medium / high / urgent |
| due_date | timestamp | nullable |
| org_id | int | FK → organizations |
| assigned_to | int | FK → users |
| created_at | timestamp | |
| is_deleted | boolean | soft delete flag |
| deleted_at | timestamp | nullable |

### refresh_tokens
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| token | varchar | hashed |
| user_id | int | FK → users |
| expires_at | timestamp | |
| revoked | boolean | |

---

## Testing

```bash
pytest tests/ -v
```

45 tests covering auth, RBAC, tasks, users, and organizations with transaction-per-test isolation.

---

## Progress

| Week | Focus | Status |
|---|---|---|
| Week 1 | FastAPI Core — CRUD, routers, schemas | ✅ |
| Week 2 | PostgreSQL — SQLAlchemy, Alembic, ORM | ✅ |
| Week 3 | Auth — JWT, bcrypt, RBAC, refresh tokens | ✅ |
| Week 4 | Multi-tenancy — orgs, members, tasks, isolation | ✅ |
| Week 5 | Code quality — services layer, logging, 45 tests | ✅ |
| Week 6 | Docker, deployment, health check, graceful shutdown | ✅ |