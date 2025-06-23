# Backend Documentation

## Overview
This backend is built with **Flask** and provides a RESTful API for a feedback management system. It uses SQLAlchemy ORM for database operations and JWT for authentication. The backend connects to a Supabase PostgreSQL database.

---

## Main Components

### 1. Flask App (`app.py`)
- **Authentication:** JWT-based login and registration for managers and employees.
- **User Roles:** Manager and Employee, with role-based access control.
- **Models:**
  - `User`: Stores user info, roles, and relationships.
  - `Feedback`: Stores feedback entries, linked to users.
- **Endpoints:**
  - `/api/auth/login` (POST): Login and receive JWT.
  - `/api/auth/register` (POST): Register a new user.
  - `/api/users/me` (GET): Get current user info.
  - `/api/team` (GET): Manager's team members.
  - `/api/feedback` (POST): Manager creates feedback.
  - `/api/feedback/<id>` (PUT): Manager updates feedback.
  - `/api/feedback/manager` (GET): All feedback given by manager.
  - `/api/feedback/employee` (GET): All feedback received by employee.
  - `/api/feedback/<id>/acknowledge` (POST): Employee acknowledges feedback.
  - `/api/dashboard/manager` (GET): Manager dashboard data.
  - `/api/dashboard/employee` (GET): Employee dashboard data.

### 2. Database Models
- **User**: id, email, password_hash, name, role, manager_id, created_at
- **Feedback**: id, manager_id, employee_id, strengths, areas_to_improve, sentiment, acknowledged, created_at, updated_at

### 3. Security
- Passwords are hashed using Werkzeug.
- JWT tokens for stateless authentication.
- CORS enabled for frontend-backend communication.

### 4. Environment Variables
- `SUPABASE_URL`, `SUPABASE_KEY`, `DATABASE_URL`, `JWT_SECRET_KEY`, `FLASK_ENV`

---

## Setup & Running

### Requirements
See [requirements.txt](../requirements.txt):
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask-JWT-Extended
- python-dotenv
- psycopg2-binary
- Werkzeug

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up `.env` with your Supabase and JWT credentials.
3. Run the app:
   ```bash
   python app.py
   ```

### Docker
See [Dockerfile](../Dockerfile):
- Python 3.9-slim base
- Installs system and Python dependencies
- Exposes port 5000
- Runs `python app.py`

Build and run:
```bash
docker build -t feedback-backend .
docker run -p 5000:5000 --env-file .env feedback-backend
```

---

## Example .env
```
SUPABASE_URL=...
SUPABASE_KEY=...
DATABASE_URL=...
JWT_SECRET_KEY=...
FLASK_ENV=development
```

---

## Notes
- The backend is stateless and can be deployed on any platform supporting Python and Docker.
- For full API details, see the [API section in the main README](../Readme.md). 