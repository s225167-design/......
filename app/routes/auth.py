#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    result = auth_service.register(username, password, email)
    if result.get('error'):
        return jsonify(result), 400

    return jsonify(result), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    result = auth_service.login(username, password)
    if result.get('error'):
        return jsonify(result), 401

    return jsonify(result), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'error': '未提供令牌'}), 401

    user = auth_service.get_user_by_token(token)
    if not user:
        return jsonify({'error': '令牌无效'}), 401

    return jsonify(user), 200
