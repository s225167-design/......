#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime


def validate_username(username):
    if not username or len(username) < 3 or len(username) > 20:
        return False, '用户名长度必须在3-20个字符之间'
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
        return False, '用户名只能包含字母、数字、下划线和中文字符'
    return True, ''


def validate_password(password):
    if not password or len(password) < 6:
        return False, '密码长度不能少于6位'
    return True, ''


def validate_email(email):
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, '邮箱格式不正确'
    return True, ''


def truncate_text(text, length=200, suffix='...'):
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length] + suffix


def safe_filename(filename):
    if not filename:
        return ''
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + '.' + ext if ext else name[:255]
    return filename
