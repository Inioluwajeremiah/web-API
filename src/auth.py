from os import access
from flask import Blueprint, request, jsonify
from importlib_metadata import email
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS, HTTP_409_CONFLICT
from src.constants.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flasgger import swag_from, Swagger
from src.Models import User, db

auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    useremail = request.json['email']
    password = request.json['password']

    if len(username) < 3:
        return jsonify({'error': 'Username cannot be less than eight characters'}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({'error': ' Weak password! It cannot be less than eight characters'}), HTTP_400_BAD_REQUEST

    # check if username is alphanumeric
    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should be alphanumeric'}), HTTP_400_BAD_REQUEST

    if not validators.email(useremail):
        return jsonify({'error': 'Email is invalid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(useremail=useremail).first() is not None:
        return jsonify({'error': 'Email already exists'}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, useremail=useremail)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": useremail
        }
    }), HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    useremail = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(useremail=useremail).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh_token,
                    'access': access_token,
                    'username': user.username,
                    'email': user.useremail
                }
            }), HTTP_200_OK
    return jsonify({'error': 'Wrong login details'}), HTTP_401_UNAUTHORIZED_ACCESS


@auth.get("/me")
@jwt_required()
def me():
    # import pdb
    # pdb.set_trace()
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'usermail': user.useremail
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify({
        'access': access_token
    }), HTTP_200_OK
