import logging
from flask import request, jsonify
from app.models.user import User
from app import db, response
from flask_jwt_extended import jwt_required

@jwt_required()
def index():
    try:
        users = User.query.all()
        return response.success_response([user.to_dict() for user in users], 'Berhasil mendapatkan data user')
    except Exception as e:
        logging.error(f"Terjadi kesalahan server: {str(e)}", exc_info=True)
        return response.error_response([], 'Terjadi kesalahan server')

def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.error_response([], 'User tidak ditemukan'), 404
        return response.success_response(user.to_dict(), 'Berhasil mendapatkan data user')
    except Exception as e:
        logging.error(f"Terjadi kesalahan server: {str(e)}", exc_info=True)
        return response.error_response([], 'Terjadi kesalahan server')
    
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.error_response([], 'User tidak ditemukan'), 404
        
        data = request.get_json(silent=True) or {}
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)

        if 'password'in data and data['password']:
            user.set_password(data['password'])

        db.session.commit()
        return response.success_response(user.to_dict(), 'Berhasil mengupdate data user')
    except Exception as e:
        logging.error(f"Terjadi kesalahan server: {str(e)}", exc_info=True)

def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response.error_response([], 'User tidak ditemukan'), 404
        
        db.session.delete(user)
        db.session.commit()

        return response.success_response(user.to_dict(), 'Berhasil menghapus data user')
    except Exception as e:
        logging.error(f"Terjadi kesalahan server: {str(e)}", exc_info=True)
        return response.error_response([], 'Terjadi kesalahan server', 500)
