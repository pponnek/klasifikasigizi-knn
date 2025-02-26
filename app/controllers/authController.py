from app.models.user import User
from app import db, jwt
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

blacklist = set()

def register():
    try:
        data = request.get_json(silent=True) or {}

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        cekDATA = [username, email, password]

        if not username or not email or not password:
            return jsonify({'data': cekDATA,
                            'error': 'Semua field wajib diisi'}), 400
        
        # Cek username/email sudah terdaftar
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            logging.warning(f'Registrasi gagal : Username "{username}" atau email "{password}" sudah terdaftar')
            return jsonify({'error': 'Username atau email sudah terdaftar'}), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


        logging.info(f'Registrasi berhasil: {username}, {email} berhasil didaftarkan')
        return jsonify({'message': 'User berhasil didaftarkan'}), 201

    except Exception as e:
        logger.error(f"Terjadi kesalahan server: {str(e)}", exc_info=True)
        return jsonify({'error': 'terjadi kesalahan server'}), 500

def login():
    try:
        data = request.get_json(silent=True) or {}

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Login gagal: Username dan password wajib diisi")
            return jsonify({'error': 'Username dan password wajib diisi'}), 400
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            logger.warning(f"Percobaan login gagal: Username '{username}' salah atau password tidak cocok")
            return jsonify({'error': 'Username atau password salah'}), 400

        # Buat token akses
        access_token = create_access_token(identity=str(user.id), additional_claims={"username": user.username})

        # Logging berhasil login
        logger.info(f"Login berhasil: Username '{username}', ID {user.id}")

        user.update_last_seen()

        return jsonify({
            'message': 'Login berhasil',
            'access_token': access_token,
            'user_id': user.id
        }), 200

    
    except Exception as e:
        logger.error(f"Kesalahan server saat login: {str(e)}", exc_info=True)
        return jsonify({'error': 'Terjadi kesalahan server'}), 500
    
@jwt_required()
def logout():
    try:
        jti = get_jwt_identity()
        blacklist.add(jti)
        User.query.filter_by(id=jti).first().update_last_seen()
        logger.info(f"Logout berhasil: ID {jti} berhasil logout")
        return jsonify({'message': 'Logout berhasil'}), 200
    
    
    except Exception as e:
        logger.error(f"Kesalahan server saat logout: {str(e)}", exc_info=True)
        return jsonify({'error': 'Terjadi kesalahan server'}), 500
    
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist