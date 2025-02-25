from flask import Blueprint, Request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return 'Hello, World!'

