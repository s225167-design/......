#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime


class UserModel:
    def __init__(self, db_path='database/forum.db'):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, username, password_hash, email=None):
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO users (username, password_hash, email, created_at) VALUES (?, ?, ?, ?)',
                (username, password_hash, email, datetime.now().isoformat())
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    def get_by_username(self, username):
        conn = self.get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    def get_by_id(self, user_id):
        conn = self.get_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    def update_last_active(self, user_id):
        conn = self.get_connection()
        conn.execute(
            'UPDATE users SET last_active = ? WHERE id = ?',
            (datetime.now().isoformat(), user_id)
        )
        conn.commit()
        conn.close()
