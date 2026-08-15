#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime


class PostModel:
    def __init__(self, db_path='database/forum.db'):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, user_id, title, content, category_id=None):
        conn = self.get_connection()
        cursor = conn.execute(
            'INSERT INTO posts (user_id, title, content, category_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, title, content, category_id, datetime.now().isoformat(), datetime.now().isoformat())
        )
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return post_id

    def get_all(self, page=1, per_page=20):
        conn = self.get_connection()
        offset = (page - 1) * per_page

        posts = conn.execute('''
            SELECT p.*, u.username, u.avatar,
                   COUNT(r.id) as reply_count
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            LEFT JOIN replies r ON p.id = r.post_id
            GROUP BY p.id
            ORDER BY p.is_pinned DESC, p.created_at DESC
            LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()

        total = conn.execute('SELECT COUNT(*) as count FROM posts').fetchone()['count']
        conn.close()

        return [dict(p) for p in posts], total

    def get_by_id(self, post_id):
        conn = self.get_connection()
        post = conn.execute('''
            SELECT p.*, u.username, u.avatar,
                   COUNT(r.id) as reply_count
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            LEFT JOIN replies r ON p.id = r.post_id
            WHERE p.id = ?
            GROUP BY p.id
        ''', (post_id,)).fetchone()

        if post:
            replies = conn.execute('''
                SELECT r.*, u.username, u.avatar
                FROM replies r
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.post_id = ?
                ORDER BY r.created_at ASC
            ''', (post_id,)).fetchall()

            result = dict(post)
            result['replies'] = [dict(r) for r in replies]
            conn.close()
            return result

        conn.close()
        return None

    def delete(self, post_id, user_id):
        conn = self.get_connection()
        post = conn.execute('SELECT user_id FROM posts WHERE id = ?', (post_id,)).fetchone()
        if not post:
            conn.close()
            return False

        if post['user_id'] != user_id:
            user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (user_id,)).fetchone()
            if not user or not user['is_admin']:
                conn.close()
                return False

        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.execute('DELETE FROM replies WHERE post_id = ?', (post_id,))
        conn.commit()
        conn.close()
        return True

    def pin(self, post_id):
        conn = self.get_connection()
        conn.execute('UPDATE posts SET is_pinned = 1 WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()

    def unpin(self, post_id):
        conn = self.get_connection()
        conn.execute('UPDATE posts SET is_pinned = 0 WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()
