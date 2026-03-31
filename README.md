# Project Management
A company manages projects and tasks assigned to users.

Architecture Overview
This project follows a layered backend architecture (FastAPI):

1. Presentation Layer (API Layer)
* Handles HTTP requests via REST endpoints
* Performs input validation
* Defines API routes

Example routes:
/auth/*
/projects/*
/tasks/*

2. Service Layer (Business Logic)
* Contains core logic such as:
      * OTP generation & verification
      * User role handling (admin, developer)
      * Task assignment rules
* Acts as a bridge between API and database

3. Data Access Layer 
* Communicates with the database
* Uses ORM
* Handles CRUD operations

4. Database Layer
Stores:
* Users
* Projects
* Tasks


# Entity Relationship (ER) Diagram
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


Relationships:
* User → Tasks: One-to-Many (assigned_to)
* Project → Tasks: One-to-Many
* User Roles: admin and developer

# Setup Instructions
1. Clone the Repository:
* git clone <repo-url>
* cd project-management

2. Create Virtual Environment and Activate:
* python -m venv venv

Activate:
* source venv/bin/activate   # Linux/Mac
* venv\Scripts\activate      # Windows

3. Install Dependencies
* pip install -r requirements.txt

4. Configure Environment Variables
* .env file

5. Run Migrations 
* alembic upgrade head

6. Start Server
* uvicorn main:app --reload
* Server runs at:
* http://127.0.0.1:8000

# Frontend Integration (Axios)
Frontend communicates with backend using Axios.

Frontend Setup:
* npm install
* npm run dev

Frontend runs at:
* http://localhost:3000

# Authentication Flow
Step 1: Request OTP
* POST /auth/request-login?email=admin@example.com
* OTP is generated
* Currently printed in terminal (development mode)
Step 2: Verify OTP
* POST /auth/verify-login
Step 3: Use Token
* Authorization: Bearer <access_token>

# Auth APIs
1. Create User:
POST /auth/create_user
2. Request Login:
POST /auth/request-login
3. Verify Login:
POST /auth/verify-login
4. Test Auth:
GET /auth/test-auth
5. List Users:
GET /auth/users

Authorization: Bearer token

# Project APIs
1. Create Project:
POST /projects
2. List Projects:
GET /projects/
3. Update Project:
POST /projects/?project_id=8&name=NewName
4. Delete Project:
DELETE /projects/{id}

# Task APIs
1. Create Task:
POST /tasks/
2. Assign Task:
PATCH /tasks/{task_id}/assign?user_id=9
3. Update Status:
PATCH /tasks/{task_id}?status=done
4. List Tasks:
GET /tasks/
