# Project Management
A company manages projects and tasks assigned to users.

🧩 Architecture Overview

This project follows a layered backend architecture (typical of FastAPI/Django REST style systems):

1. Presentation Layer (API Layer)
Handles HTTP requests via REST endpoints
Performs input validation
Example routes:
/auth/*
/projects/*
/tasks/*
2. Service Layer (Business Logic)
Contains core logic such as:
OTP generation & verification
User role handling (admin, developer)
Task assignment rules
Acts as a bridge between API and database
3. Data Access Layer (DAL / ORM)
Communicates with the database
Uses ORM (e.g., SQLAlchemy / Django ORM)
Handles CRUD operations
4. Database Layer
Stores:
Users
Projects
Tasks
Authentication tokens
🗂️ Entity Relationship (ER) Diagram
+------------+        +-------------+        +-------------+
|   Users    |        |  Projects   |        |    Tasks    |
+------------+        +-------------+        +-------------+
| id (PK)    |        | id (PK)     |        | id (PK)     |
| name       |        | name        |        | title       |
| email      |        | description |        | description |
| role       |        +-------------+        | status      |
+------------+                |              | due_date    |
      |                       |              | project_id  |
      |                       |              | assigned_to |
      |                       |              +-------------+
      |                       |                     |
      +-----------------------+---------------------+
              (User can be assigned tasks)
              (Project has many tasks)
Relationships:
User → Tasks: One-to-Many (assigned_to)
Project → Tasks: One-to-Many
User Roles: Controls permissions (admin / developer)
⚙️ Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd project-management
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create .env file:

DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
5. Run Migrations (if applicable)
alembic upgrade head
6. Start Server
uvicorn main:app --reload

Server runs at:

http://127.0.0.1:8000

🌐 Frontend Integration (Axios)

This project includes a frontend application (running on http://localhost:3000) that communicates with the backend API using Axios.

🚀 Frontend Setup
npm install
npm run dev

Frontend runs at:

http://localhost:3000

🔐 Authentication Flow
Step 1: Request OTP
POST /auth/request-login?email=admin@example.com
OTP is generated
Currently printed in terminal (dev mode)
Step 2: Verify OTP
POST /auth/verify-login

Params:

email
otp
otp_token

Response:

{
  "access_token": "...",
  "token_type": "bearer"
}
Step 3: Use Token
Authorization: Bearer <access_token>
📡 API Documentation
🔹 Auth APIs
Request Login
POST /auth/request-login
Verify Login
POST /auth/verify-login
Test Auth
GET /auth/test-auth
👤 User APIs
List Users
GET /auth/users
Authorization: Bearer token
Create User
POST /auth/create_user
Body:
{
  "name": "user",
  "email": "user@example.com",
  "role": "developer"
}
📁 Project APIs
Create Project
POST /projects
Body:
{
  "name": "API",
  "description": "interface"
}
List Projects
GET /projects/
Update Project
POST /projects/?project_id=8&name=NewName
Delete Project
DELETE /projects/{id}
✅ Task APIs
Create Task
POST /tasks/

Body:

{
  "title": "validation",
  "project_id": 8,
  "assigned_to": null,
  "description": "new task",
  "status": "in_progress",
  "due_date": "2026-03-31"
}
Assign Task
PATCH /tasks/{task_id}/assign?user_id=9
Update Status
PATCH /tasks/{task_id}?status=done
List Tasks
GET /tasks/
