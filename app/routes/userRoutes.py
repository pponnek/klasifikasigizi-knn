import logging
from flask import Blueprint, request
from app.controllers import userController
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    logging.info('GET /user - Fetching all users')
    return userController.index()

@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    logging.info(f'GET /user/{id} - Fetching user with id {id}')
    return userController.get_user(id)

@user_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    logging.info(f'PUT /user/{id} - Updating user with id {id}')
    data = request.get_json(silent=True) or {}
    if not data:
        return {'error': 'data tidak ditemukan'}, 400
    return userController.update_user(id)

@user_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    logging.info(f'DELETE /user/{id} - Deleting user with id {id}')
    return userController.delete_user(id)