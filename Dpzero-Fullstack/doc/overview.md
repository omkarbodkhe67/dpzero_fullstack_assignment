# Project Overview

## Feedback Management System

This project is a lightweight feedback management system for internal team communication between managers and employees. It consists of a Flask backend and a React (CDN) frontend, integrated with a Supabase PostgreSQL database.

---

## Architecture

- **Backend:** Flask REST API (see [backend.md](./backend.md))
- **Frontend:** React single-page app in a single HTML file (see [frontend.md](./frontend.md))
- **Database:** Supabase PostgreSQL
- **Containerization:** Docker for backend

---

## Tech Stack

- **Frontend:** React 18, Tailwind CSS, Axios, Font Awesome
- **Backend:** Python 3.9, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- **Database:** Supabase PostgreSQL
- **Other:** Docker, python-dotenv

---

## How It Works

- **Authentication:** JWT-based login for managers and employees
- **Role-based Access:** Managers can give feedback to their team; employees can view and acknowledge feedback
- **API:** RESTful endpoints for authentication, team management, feedback, and dashboards
- **Frontend:** Communicates with backend via Axios, manages auth state with React Context
- **Deployment:** Backend can be run locally or in Docker; frontend is static and can be hosted anywhere

---

## Documentation
- [Backend Documentation](./backend.md)
- [Frontend Documentation](./frontend.md)

For detailed API, setup, and deployment instructions, see the main [Readme.md](../Readme.md). 