#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import random
from datetime import datetime, timedelta
import bcrypt


def seed_database(db_path='database/forum.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    users = ['alice', 'bob', 'charlie', 'diana', 'eve', 'frank', 'grace', 'henry']
    for i, username in enumerate(users, start=4):
        password_hash = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            'INSERT OR IGNORE INTO users (username, password_hash, email, created_at) VALUES (?, ?, ?, ?)',
            (username, password_hash, f'{username}@forum.com', datetime.now().isoformat())
        )

    posts_titles = [
        'Python 3.11 新特性介绍',
        'Flask 与 Django 对比分析',
        'SQLite 性能优化技巧',
        'JWT 认证详解',
        'Docker 容器化部署实践',
        '前端框架选择指南',
        'Git 版本控制最佳实践',
        'Linux 服务器运维基础',
        '数据库索引优化策略',
        'RESTful API 设计规范'
    ]

    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    for i, title in enumerate(posts_titles):
        user_id = random.choice(user_ids)
        content = f'这是关于 {title} 的详细内容。' * 5
        created_at = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 24))
        is_pinned = 1 if i < 2 else 0
        cursor.execute(
            'INSERT INTO posts (user_id, title, content, is_pinned, created_at) VALUES (?, ?, ?, ?, ?)',
            (user_id, title, content, is_pinned, created_at.isoformat())
        )

    cursor.execute('SELECT id FROM posts')
    post_ids = [row[0] for row in cursor.fetchall()]

    for post_id in post_ids:
        for _ in range(random.randint(0, 5)):
            user_id = random.choice(user_ids)
            content = f'这是回复内容 #{random.randint(1, 100)}'
            created_at = datetime.now() - timedelta(days=random.randint(0, 10), hours=random.randint(0, 24))
            cursor.execute(
                'INSERT INTO replies (post_id, user_id, content, created_at) VALUES (?, ?, ?, ?)',
                (post_id, user_id, content, created_at.isoformat())
            )

    conn.commit()
    conn.close()
    print('✅ 示例数据填充完成！')


if __name__ == '__main__':
    seed_database()
