#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import bcrypt
from datetime import datetime, timedelta
import os
from app.models.user import UserModel


class AuthService:
    def __init__(self):
        self.user_model = UserModel()
        self.secret = os.getenv('JWT_SECRET', 'jwt-secret-key')
        self.expiration = int(os.getenv('JWT_EXPIRATION', 86400))

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def generate_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.expiration),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.InvalidTokenError:
            return None

    def register(self, username, password, email=None):
        existing = self.user_model.get_by_username(username)
        if existing:
            return {'error': '用户名已存在'}

        password_hash = self.hash_password(password)
        user_id = self.user_model.create(username, password_hash, email)

        if not user_id:
            return {'error': '注册失败'}

        token = self.generate_token(user_id)
        return {
            'user_id': user_id,
            'username': username,
            'token': token
        }

    def login(self, username, password):
        user = self.user_model.get_by_username(username)
        if not user:
            return {'error': '用户名或密码错误'}

        if not self.verify_password(password, user['password_hash']):
            return {'error': '用户名或密码错误'}

        token = self.generate_token(user['id'])
        self.user_model.update_last_active(user['id'])

        return {
            'user_id': user['id'],
            'username': user['username'],
            'token': token,
            'is_admin': user.get('is_admin', False)
        }

    def get_user_by_token(self, token):
        user_id = self.decode_token(token)
        if not user_id:
            return None

        user = self.user_model.get_by_id(user_id)
        if user:
            user.pop('password_hash', None)
        return user
