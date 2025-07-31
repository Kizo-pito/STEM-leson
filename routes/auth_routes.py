from flask import Blueprint, request, jsonify
from models.user import db, User
from datetime import datetime
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    full_name = data.get('full_name')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username hoặc email đã tồn tại"}), 400

    user = User(username=username, email=email, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Đăng ký thành công"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username')
    password = data.get('password')

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Sai thông tin đăng nhập"}), 401

    if not user.is_active:
        return jsonify({"error": "Tài khoản bị vô hiệu hóa"}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()
    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Đăng nhập thành công",
        "user": user.to_dict()
    }), 200
