from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .validations import *
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    _, err = validate_signup_data(data)
    if err:
        return jsonify({'error': err}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Username already exists'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(email=data['email'], first_name=data['first_name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    _, err = validate_login_data(data)
    if err:
        return jsonify({'error': err}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
