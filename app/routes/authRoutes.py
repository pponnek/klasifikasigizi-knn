from flask import Blueprint, Request
from app.controllers import authController

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    return authController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return authController.login()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return authController.logout()
