#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime


class ReplyModel:
    def __init__(self, db_path='database/forum.db'):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, post_id, user_id, content):
        conn = self.get_connection()
        cursor = conn.execute(
            'INSERT INTO replies (post_id, user_id, content, created_at) VALUES (?, ?, ?, ?)',
            (post_id, user_id, content, datetime.now().isoformat())
        )
        conn.commit()

        conn.execute(
            'UPDATE posts SET reply_count = reply_count + 1, updated_at = ? WHERE id = ?',
            (datetime.now().isoformat(), post_id)
        )
        conn.commit()

        reply_id = cursor.lastrowid
        conn.close()
        return reply_id

    def delete(self, reply_id, user_id):
        conn = self.get_connection()
        reply = conn.execute('SELECT post_id, user_id FROM replies WHERE id = ?', (reply_id,)).fetchone()
        if not reply:
            conn.close()
            return False

        if reply['user_id'] != user_id:
            user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (user_id,)).fetchone()
            if not user or not user['is_admin']:
                conn.close()
                return False

        conn.execute('DELETE FROM replies WHERE id = ?', (reply_id,))
        conn.execute(
            'UPDATE posts SET reply_count = reply_count - 1 WHERE id = ?',
            (reply['post_id'],)
        )
        conn.commit()
        conn.close()
        return True
