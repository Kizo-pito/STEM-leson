from flask import request, jsonify, session
from models.user import User, db

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Register successful'}), 201

def login():
    # 获取请求中的json数据
    data = request.get_json()
    # 获取json数据中的用户名
    username = data.get('username')
    # 获取json数据中的密码
    password = data.get('password')
    # 根据用户名查询用户
    user = User.query.filter_by(username=username).first()
    # 如果用户不存在或者密码不正确，返回错误信息
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    # 将用户id存入session
    session['user_id'] = user.id
    # 返回登录成功信息
    return jsonify({'message': 'Login successful'}), 200

def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200