# Feedback System

A lightweight feedback management system for internal team communication between managers and employees, built with React frontend and Flask backend, integrated with Supabase PostgreSQL.

## 🚀 Demo Credentials

**Manager Account:**
- Email: `manager@company.com`
- Password: `password123`

**Employee Account:**
- Email: `alice@company.com`  
- Password: `password123`

## 🏗 Tech Stack

**Frontend:**
- React 18 (Vanilla JS with Babel)
- Tailwind CSS for styling
- Axios for API calls
- Font Awesome for icons

**Backend:**
- Python 3.9
- Flask web framework
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-origin requests)
- PostgreSQL (Supabase)

**Database:**
- Supabase PostgreSQL with ORM schema

## 📁 Project Structure

```
feedback-system/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Docker configuration
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── index.html         # React application
│   └── package.json       # Frontend dependencies info
└── README.md
```

## 🛠 Setup Instructions

### Prerequisites
- Python 3.9+
- Docker (for containerization)
- Supabase account
- Git

### 1. Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Settings → Database
3. Copy the connection string
4. Note down your project URL and anon key

### 2. Backend Setup

1. **Clone and navigate to backend:**
```bash
mkdir feedback-system && cd feedback-system
mkdir backend && cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment configuration:**
```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
DATABASE_URL=postgresql://postgres:your-password@db.your-project.supabase.co:5432/postgres
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
FLASK_ENV=development
```

5. **Run the application:**
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd ../frontend
```

2. **Serve the HTML file:**
```bash
# Using Python
python -m http.server 3000

# Or using Node.js (if you have it)
npx serve . -p 3000

# Or simply open index.html in your browser
```

The frontend will be available at `http://localhost:3000`

### 4. Docker Setup (Backend Only)

1. **Build Docker image:**
```bash
cd backend
docker build -t feedback-system-backend .
```

2. **Run Docker container:**
```bash
docker run -p 5000:5000 --env-file .env feedback-system-backend
```

## 📊 Database Schema

The application uses SQLAlchemy ORM with the following models:

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password_hash`
- `name`
- `role` (manager/employee)
- `manager_id` (Foreign Key to Users)
- `created_at`

### Feedback Table
- `id` (Primary Key)
- `manager_id` (Foreign Key to Users)
- `employee_id` (Foreign Key to Users)
- `strengths` (Text)
- `areas_to_improve` (Text)
- `sentiment` (positive/neutral/negative)
- `acknowledged` (Boolean)
- `created_at`
- `updated_at`

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/users/me` - Get current user

### Team Management
- `GET /api/team` - Get team members (Manager only)

### Feedback Management
- `POST /api/feedback` - Create feedback (Manager only)
- `PUT /api/feedback/<id>` - Update feedback (Manager only)
- `GET /api/feedback/manager` - Get all feedback given by manager
- `GET /api/feedback/employee` - Get all feedback received by employee
- `POST /api/feedback/<id>/acknowledge` - Acknowledge feedback (Employee only)

### Dashboard
- `GET /api/dashboard/manager` - Manager dashboard data
- `GET /api/dashboard/employee` - Employee dashboard data

## ✨ Features Implemented

### Core Features (MVP)
- ✅ **Authentication & Roles**: Manager and Employee roles with secure login
- ✅ **Feedback Submission**: Structured feedback with strengths, improvements, and sentiment
- ✅ **Feedback Visibility**: Role-based access with proper data isolation
- ✅ **Feedback History**: Complete timeline of feedback for both roles
- ✅ **Feedback Management**: Managers can edit/update their feedback
- ✅ **Acknowledgment System**: Employees can acknowledge received feedback
- ✅ **Dashboard Views**: Different dashboards for managers and employees

### Bonus Features
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **Real-time Updates**: Automatic refresh of data
- ✅ **Sentiment Analysis**: Visual sentiment indicators
- ✅ **Clean UI/UX**: Intuitive and empathetic design
- ✅ **Docker Support**: Containerized backend deployment

## 🎨 Design Decisions

### Frontend Architecture
- **Single HTML File**: Simplified deployment without build process
- **React with CDN**: Faster development without complex tooling
- **Tailwind CSS**: Rapid UI development with consistent design
- **Context API**: State management for authentication
- **Axios**: HTTP client with interceptors for authentication

### Backend Architecture
- **Flask**: Lightweight and flexible Python web framework
- **SQLAlchemy ORM**: Database abstraction with relationship management
- **JWT Authentication**: Stateless token-based authentication
- **Role-based Access Control**: Endpoint-level authorization
- **RESTful API Design**: Clear and predictable API structure

### Database Design
- **Relational Structure**: Proper foreign key relationships
- **Audit Trail**: Created/updated timestamps for feedback
- **Data Integrity**: Constraints and validations
- **Scalable Schema**: Designed for future feature additions

### Security Considerations
- **Password Hashing**: Werkzeug secure password hashing
- **JWT Tokens**: Secure token-based authentication
- **CORS Configuration**: Controlled cross-origin access
- **Input Validation**: Server-side request validation
- **Role Enforcement**: Strict role-based access control

## 🚀 Deployment

### Backend Deployment (using Docker)
```bash
# Build and push to registry
docker build -t your-registry/feedback-backend .
docker push your-registry/feedback-backend

# Deploy to your platform (Railway, Render, etc.)
```

### Frontend Deployment
The frontend is a static HTML file that can be deployed to:
- Netlify
- Vercel  
- GitHub Pages
- Any static hosting service

## 🧪 Testing

### Manual Testing Checklist
- [ ] Manager login and dashboard
- [ ] Employee login and dashboard
- [ ] Create feedback for team members
- [ ] Edit existing feedback
- [ ] Employee feedback acknowledgment
- [ ] Role-based access restrictions
- [ ] Responsive design on mobile

### API Testing
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"manager@company.com","password":"password123"}'

# Create feedback (replace TOKEN)
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"employee_id":2,"strengths":"Great communication","areas_to_improve":"Time management","sentiment":"positive"}'
```

## 🤝 AI Assistance Disclosure

This project was developed with assistance from Claude AI for:
- Code structure and best practices
- API endpoint design
- Frontend component architecture
- Documentation creation

All code has been reviewed and tested to ensure functionality and security.

## 📝 Future Enhancements

- Email notifications for new feedback
- Peer feedback system
- Feedback analytics and reporting
- Export functionality (PDF/Excel)
- Mobile app version
- Integration with Slack/Teams
- Feedback templates
- Performance review cycles

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify Supabase credentials in `.env`
   - Check database URL format
   - Ensure Supabase project is active

2. **CORS Issues**
   - Verify frontend URL in Flask-CORS configuration
   - Check browser developer console for errors

3. **Authentication Failures**
   - Verify JWT secret key is set
   - Check token expiration settings
   - Clear browser localStorage if needed

4. **Docker Issues**
   - Ensure `.env` file is properly configured
   - Check Docker container logs: `docker logs <container-id>`

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review API endpoint documentation
3. Verify environment configuration
4. Check browser developer console for frontend errors
5. Review Flask application logs for backend errors

## 📄 License

This project is created for educational purposes as part of a technical assessment.