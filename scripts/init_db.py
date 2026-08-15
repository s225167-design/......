#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime
import bcrypt


def init_database(db_path='database/forum.db'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            avatar TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_active DATETIME
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category_id INTEGER,
            is_pinned INTEGER DEFAULT 0,
            is_essence INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            'INSERT INTO users (username, password_hash, email, is_admin) VALUES (?, ?, ?, ?)',
            ('admin', admin_password, 'admin@forum.com', 1)
        )

        cursor.execute(
            'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
            ('user1', bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 'user1@forum.com')
        )

        cursor.execute(
            'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
            ('user2', bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 'user2@forum.com')
        )

        cursor.execute('''
            INSERT INTO categories (name, description) VALUES
            ('技术交流', '讨论技术相关问题'),
            ('生活分享', '分享生活点滴'),
            ('提问求助', '寻求帮助和解答')
        ''')

        cursor.execute('''
            INSERT INTO posts (user_id, title, content, is_pinned, created_at) VALUES
            (1, '📌 欢迎来到论坛 V5', '这是企业级全栈论坛的第五个版本。包含完整的用户认证、帖子管理、回复系统。', 1, datetime('now', '-2 days')),
            (2, '第一次发帖测试', '这个论坛真好用！界面简洁，功能完整。', 0, datetime('now', '-1 days')),
            (3, '求助：关于Flask的问题', '有人知道Flask如何处理文件上传吗？', 0, datetime('now'))
        ''')

        cursor.execute('''
            INSERT INTO replies (post_id, user_id, content, created_at) VALUES
            (1, 2, '欢迎！这个论坛确实很棒！', datetime('now', '-1 days', '+2 hours')),
            (1, 3, '功能很完整，赞一个！', datetime('now', '-1 days', '+5 hours')),
            (2, 1, '谢谢支持！有什么建议可以提出来。', datetime('now', '-12 hours')),
            (3, 1, '可以使用 Flask 的 request.files 来处理。', datetime('now', '-6 hours'))
        ''')

    conn.commit()
    conn.close()
    print('✅ 数据库初始化完成！')
    print('👤 管理员账号: admin / admin123')


if __name__ == '__main__':
    init_database()
