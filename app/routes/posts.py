#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.services.auth_service import AuthService

posts_bp = Blueprint('posts', __name__)
post_service = PostService()
auth_service = AuthService()


@posts_bp.route('/', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    posts = post_service.get_posts(page, per_page)
    return jsonify(posts), 200


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = post_service.get_post(post_id)
    if not post:
        return jsonify({'error': '帖子不存在'}), 404
    return jsonify(post), 200


@posts_bp.route('/', methods=['POST'])
def create_post():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = auth_service.get_user_by_token(token)

    if not user:
        return jsonify({'error': '请先登录'}), 401

    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': '标题和内容不能为空'}), 400

    post = post_service.create_post(user['id'], title, content)
    return jsonify(post), 201


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = auth_service.get_user_by_token(token)

    if not user:
        return jsonify({'error': '请先登录'}), 401

    if post_service.delete_post(post_id, user['id']):
        return jsonify({'message': '删除成功'}), 200

    return jsonify({'error': '删除失败，可能没有权限'}), 403
