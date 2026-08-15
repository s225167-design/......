#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.services.auth_service import AuthService

replies_bp = Blueprint('replies', __name__)
post_service = PostService()
auth_service = AuthService()


@replies_bp.route('/', methods=['POST'])
def create_reply():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = auth_service.get_user_by_token(token)

    if not user:
        return jsonify({'error': '请先登录'}), 401

    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content', '').strip()

    if not post_id or not content:
        return jsonify({'error': '参数不完整'}), 400

    reply = post_service.create_reply(post_id, user['id'], content)
    if not reply:
        return jsonify({'error': '帖子不存在'}), 404

    return jsonify(reply), 201


@replies_bp.route('/<int:reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = auth_service.get_user_by_token(token)

    if not user:
        return jsonify({'error': '请先登录'}), 401

    if post_service.delete_reply(reply_id, user['id']):
        return jsonify({'message': '删除成功'}), 200

    return jsonify({'error': '删除失败，可能没有权限'}), 403
