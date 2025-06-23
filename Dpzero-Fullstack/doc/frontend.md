# Frontend Documentation

## Overview
The frontend is a single-page React application (served via a single `index.html`) for the feedback management system. It uses React 18 (via CDN), Tailwind CSS for styling, Axios for API calls, and Font Awesome for icons. No build step is required.

---

## Main Components

### 1. Authentication
- **Context API** is used for managing authentication state.
- JWT tokens are stored in localStorage and attached to Axios requests.
- Login and logout functionality is provided.

### 2. UI Components
- **LoginForm**: Handles user login.
- **Header**: Displays app title, user info, and logout button.
- **ManagerDashboard**: For managers to view team, give feedback, and see dashboard data.
- **EmployeeDashboard**: For employees to view received feedback and dashboard data.
- **Feedback forms**: For creating and editing feedback.
- **Feedback lists**: For viewing feedback history.

### 3. API Integration
- All API calls are made to the Flask backend (default: `http://localhost:5000/api`).
- Axios is used for HTTP requests, with JWT token attached in headers.

### 4. Styling
- **Tailwind CSS** is used for rapid, responsive UI development.
- **Font Awesome** is used for icons.

---

## Setup & Running

### Requirements
See [package.json](../package.json):
- React 18
- ReactDOM 18
- Axios

### Local Development
1. Serve the frontend:
   ```bash
   python -m http.server 3000
   ```
   or open `index.html` directly in your browser.

### Project Scripts
- `start`/`dev`: Serve with Python HTTP server on port 3000.
- `build`: No build step required.

---

## Notes
- The frontend is fully static and can be deployed to any static hosting service (Netlify, Vercel, GitHub Pages, etc.).
- Demo credentials are provided on the login page for quick testing.
- For API details, see the backend documentation and main README. 