# SaaS Backend

A production-grade multi-tenant SaaS Backend built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

## Features
- JWT Authentication with refresh token rotation
- Role-Based Access Control (RBAC) — admin/member roles
- Multi-tenant architecture with strict data isolation
- Organization & membership system
- Task management with soft deletes, priority, and due dates
- Pagination on all list endpoints
- Connection pooling with SQLAlchemy
- Pydantic v2 validation with custom validators
- Modular router structure
- Proper HTTP error handling (400, 401, 403, 404, 422)

## Tech Stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- python-jose (JWT)
- bcrypt (password hashing)
- Pydantic v2
- uvicorn

## Project Structure
SaaS-Backend/
├── main.py
├── db.py
├── schemas.py
├── sql_practice.sql
├── requirements.txt
├── .env                        # never committed
├── .env.example
├── .gitignore
├── alembic.ini
├── auth/
│   ├── dependencies.py
│   ├── hashing.py
│   └── tokens.py
├── crud/
│   └── users.py
├── models/
│   ├── organization.py
│   ├── organization_member.py
│   ├── refresh_token.py
│   ├── task.py
│   └── user.py
├── routers/
│   ├── auth.py
│   ├── organizations.py
|   ├── tasks.py
│   └── users.py
└── alembic/
    └── versions/

## Setup
```bash
git clone https://github.com/saksham-42/Saas-Backend.git
cd SaaS-Backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```
Create `.env` file:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/yourdbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
EXPIRE_MINUTES=30

Run migrations:
```bash
alembic upgrade head
```

Start server:
```bash
uvicorn main:app --reload
```
## Database Schema

### users
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| name | varchar | min 2 chars |
| age | int | 18–75 |
| email | varchar | unique, indexed |
| hashed_password | varchar | bcrypt |
| role | varchar | admin / member |
| org_id | int | FK → organizations |

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
| due_date | timestamp | nullable, must be future |
| org_id | int | FK → organizations |
| assigned_to | int | FK → users, must be org member |
| created_at | timestamp | |
| is_deleted | boolean | soft delete flag |
| deleted_at | timestamp | nullable |

## API Endpoints

### Users
| Method | Endpoint | Description |
|---|---|---|
| POST | /users/ | Add new user |
| GET | /users/ | List all users |
| GET | /users/{id} | Get user by id |
| PUT | /users/{id} | Update user |
| DELETE | /users/{id} | Delete user (admin only) |
| GET | /users/me/tasks | All tasks assigned to me across orgs |

### Auth
| Method | Endpoint | Description |
|---|---|---|
| GET | /users/me | Get current logged-in user |
| POST | /auth/register | Register new user with password |
| POST | /auth/login | Login, returns JWT |
| POST | /auth/refresh | Refresh access token |
| POST | /auth/logout | Revoke refresh token |

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
| GET | /organization/{id}/tasks | List tasks (filter by status as well) |
| PUT | /organization/{id}/tasks/{task_id} | Update task status |
| PATCH | /organization/{id}/tasks/{task_id}/assign | Assign task to member |
| DELETE | /organization/{id}/tasks/{task_id} | Soft delete task |

## Progress
| Week | Focus | Status |
|---|---|---|
| Week 1 | FastAPI Core — CRUD, routers, schemas | ✅ |
| Week 2 | PostgreSQL — SQLAlchemy, Alembic, ORM | ✅ |
| Week 3 | Auth — JWT, bcrypt, RBAC, refresh tokens | ✅ |
| Week 4 | Multi-tenancy — orgs, members, tasks, isolation | ✅ |
| Week 5 | Coming soon | 🔜 |
