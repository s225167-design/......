#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()


def create_app(config_name='default'):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])

    CORS(app)

    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.replies import replies_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(replies_bp, url_prefix='/api/replies')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.errorhandler(404)
    def not_found(e):
        return {'error': '资源不存在'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': '服务器内部错误'}, 500

    @app.errorhandler(403)
    def forbidden(e):
        return {'error': '没有权限'}, 403

    return app
