from flask import Blueprint, request, jsonify
from models.user_model import db, bcrypt, User

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# REGISTER ENDPOINT
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered!'}), 400

    # Hash password and save new user
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


# LOGIN ENDPOINT
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"message": "Email not found"}), 401

    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({"message": "Login successful!"})

