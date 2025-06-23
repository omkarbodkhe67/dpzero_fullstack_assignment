from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
print("JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])
# Supabase PostgreSQL connection
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'manager' or 'employee'
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', remote_side=[id], backref='team_members')
    feedback_given = db.relationship('Feedback', foreign_keys='Feedback.manager_id', backref='manager')
    feedback_received = db.relationship('Feedback', foreign_keys='Feedback.employee_id', backref='employee')

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    strengths = db.Column(db.Text, nullable=False)
    areas_to_improve = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)  # 'positive', 'neutral', 'negative'
    acknowledged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Helper functions
def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Check if users already exist
    if User.query.first():
        return
    
    # Create sample manager
    manager = User(
        email='manager@company.com',
        password_hash=generate_password_hash('password123'),
        name='John Manager',
        role='manager'
    )
    db.session.add(manager)
    db.session.commit()
    
    # Create sample employees
    employees = [
        User(
            email='alice@company.com',
            password_hash=generate_password_hash('password123'),
            name='Alice Smith',
            role='employee',
            manager_id=manager.id
        ),
        User(
            email='bob@company.com',
            password_hash=generate_password_hash('password123'),
            name='Bob Johnson',
            role='employee',
            manager_id=manager.id
        )
    ]
    
    for emp in employees:
        db.session.add(emp)
    
    db.session.commit()
    print("Database initialized with sample data!")

# Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role', 'employee')
    manager_id = data.get('manager_id')
    
    if not email or not password or not name:
        return jsonify({'error': 'Email, password, and name required'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        name=name,
        role=role,
        manager_id=manager_id
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'manager_id': user.manager_id
    })

@app.route('/api/team', methods=['GET'])
@jwt_required()
def get_team_members():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    team_members = User.query.filter_by(manager_id=user_id).all()
    
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'email': member.email,
        'role': member.role
    } for member in team_members])

@app.route('/api/feedback', methods=['POST'])
@jwt_required()
def create_feedback():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'manager':
        return jsonify({'error': 'Only managers can create feedback'}), 403
    
    data = request.get_json()
    employee_id = data.get('employee_id')
    strengths = data.get('strengths')
    areas_to_improve = data.get('areas_to_improve')
    sentiment = data.get('sentiment')
    
    if not all([employee_id, strengths, areas_to_improve, sentiment]):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Verify employee is in manager's team
    employee = User.query.filter_by(id=employee_id, manager_id=user_id).first()
    if not employee:
        return jsonify({'error': 'Employee not in your team'}), 403
    
    feedback = Feedback(
        manager_id=user_id,
        employee_id=employee_id,
        strengths=strengths,
        areas_to_improve=areas_to_improve,
        sentiment=sentiment
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback created successfully'}), 201

@app.route('/api/feedback/<int:feedback_id>', methods=['PUT'])
@jwt_required()
def update_feedback(feedback_id):
    user_id = int(get_jwt_identity())
    feedback = Feedback.query.get(feedback_id)
    
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    
    if feedback.manager_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    feedback.strengths = data.get('strengths', feedback.strengths)
    feedback.areas_to_improve = data.get('areas_to_improve', feedback.areas_to_improve)
    feedback.sentiment = data.get('sentiment', feedback.sentiment)
    feedback.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Feedback updated successfully'})

@app.route('/api/feedback/manager', methods=['GET'])
@jwt_required()
def get_manager_feedback():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    feedback_list = db.session.query(Feedback, User).join(
        User, Feedback.employee_id == User.id
    ).filter(Feedback.manager_id == user_id).all()
    
    return jsonify([{
        'id': feedback.id,
        'employee_name': employee.name,
        'employee_id': employee.id,
        'strengths': feedback.strengths,
        'areas_to_improve': feedback.areas_to_improve,
        'sentiment': feedback.sentiment,
        'acknowledged': feedback.acknowledged,
        'created_at': feedback.created_at.isoformat(),
        'updated_at': feedback.updated_at.isoformat()
    } for feedback, employee in feedback_list])

@app.route('/api/feedback/employee', methods=['GET'])
@jwt_required()
def get_employee_feedback():
    user_id = int(get_jwt_identity())
    
    feedback_list = db.session.query(Feedback, User).join(
        User, Feedback.manager_id == User.id
    ).filter(Feedback.employee_id == user_id).all()
    
    return jsonify([{
        'id': feedback.id,
        'manager_name': manager.name,
        'strengths': feedback.strengths,
        'areas_to_improve': feedback.areas_to_improve,
        'sentiment': feedback.sentiment,
        'acknowledged': feedback.acknowledged,
        'created_at': feedback.created_at.isoformat(),
        'updated_at': feedback.updated_at.isoformat()
    } for feedback, manager in feedback_list])

@app.route('/api/feedback/<int:feedback_id>/acknowledge', methods=['POST'])
@jwt_required()
def acknowledge_feedback(feedback_id):
    user_id = int(get_jwt_identity())
    feedback = Feedback.query.get(feedback_id)
    
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    
    if feedback.employee_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    feedback.acknowledged = True
    db.session.commit()
    
    return jsonify({'message': 'Feedback acknowledged'})

@app.route('/api/dashboard/manager', methods=['GET'])
@jwt_required()
def manager_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get team overview
    team_count = User.query.filter_by(manager_id=user_id).count()
    total_feedback = Feedback.query.filter_by(manager_id=user_id).count()
    
    # Sentiment breakdown
    sentiment_stats = db.session.query(
        Feedback.sentiment,
        db.func.count(Feedback.id)
    ).filter_by(manager_id=user_id).group_by(Feedback.sentiment).all()
    
    sentiment_counts = {sentiment: count for sentiment, count in sentiment_stats}
    
    return jsonify({
        'team_count': team_count,
        'total_feedback': total_feedback,
        'sentiment_breakdown': sentiment_counts
    })

@app.route('/api/dashboard/employee', methods=['GET'])
@jwt_required()
def employee_dashboard():
    user_id = int(get_jwt_identity())
    
    total_feedback = Feedback.query.filter_by(employee_id=user_id).count()
    acknowledged_feedback = Feedback.query.filter_by(
        employee_id=user_id, acknowledged=True
    ).count()
    
    # Recent feedback
    recent_feedback = Feedback.query.filter_by(
        employee_id=user_id
    ).order_by(Feedback.created_at.desc()).limit(5).all()
    
    return jsonify({
        'total_feedback': total_feedback,
        'acknowledged_feedback': acknowledged_feedback,
        'pending_feedback': total_feedback - acknowledged_feedback,
        'recent_feedback_count': len(recent_feedback)
    })

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)