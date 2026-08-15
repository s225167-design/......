#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.services.auth_service import AuthService
from functools import wraps

admin_bp = Blueprint('admin', __name__)
post_service = PostService()
auth_service = AuthService()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = auth_service.get_user_by_token(token)

        if not user or not user.get('is_admin'):
            return jsonify({'error': '需要管理员权限'}), 403

        return f(*args, **kwargs)

    return decorated


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    stats = post_service.get_stats()
    return jsonify(stats), 200


@admin_bp.route('/posts', methods=['GET'])
@admin_required
def get_all_posts():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))

    posts = post_service.get_all_posts_admin(page, per_page)
    return jsonify(posts), 200
