#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.models.post import PostModel
from app.models.reply import ReplyModel
from app.models.user import UserModel


class PostService:
    def __init__(self):
        self.post_model = PostModel()
        self.reply_model = ReplyModel()
        self.user_model = UserModel()

    def get_posts(self, page=1, per_page=20):
        posts, total = self.post_model.get_all(page, per_page)
        return {
            'data': posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }

    def get_post(self, post_id):
        return self.post_model.get_by_id(post_id)

    def create_post(self, user_id, title, content):
        post_id = self.post_model.create(user_id, title, content)
        post = self.post_model.get_by_id(post_id)
        return post

    def delete_post(self, post_id, user_id):
        return self.post_model.delete(post_id, user_id)

    def create_reply(self, post_id, user_id, content):
        post = self.post_model.get_by_id(post_id)
        if not post:
            return None

        reply_id = self.reply_model.create(post_id, user_id, content)
        return {'id': reply_id, 'post_id': post_id, 'content': content}

    def delete_reply(self, reply_id, user_id):
        return self.reply_model.delete(reply_id, user_id)

    def get_stats(self):
        conn = self.post_model.get_connection()

        total_posts = conn.execute('SELECT COUNT(*) as count FROM posts').fetchone()['count']
        total_replies = conn.execute('SELECT COUNT(*) as count FROM replies').fetchone()['count']
        total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']

        conn.close()

        return {
            'total_posts': total_posts,
            'total_replies': total_replies,
            'total_users': total_users
        }

    def get_all_posts_admin(self, page=1, per_page=50):
        posts, total = self.post_model.get_all(page, per_page)
        return {
            'data': posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }
