# 📬 论坛 V5 - 企业级全栈论坛

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ 功能特点

### 核心功能
- ✅ 用户注册/登录 (JWT认证)
- ✅ 发帖/回复/删除
- ✅ 分类管理
- ✅ 置顶/精华/热门
- ✅ 用户个人主页
- ✅ 头像上传
- ✅ 搜索功能
- ✅ 管理员后台
- ✅ 数据统计

### 技术亮点
- 🔒 JWT Token 认证
- 📊 SQLite + Redis 缓存
- 🎨 响应式设计 (移动优先)
- 🌙 暗色模式
- 🌐 国际化支持
- 🚀 高性能

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 后端 | Python 3.11 + Flask 3.0 |
| 数据库 | SQLite / PostgreSQL |
| 缓存 | Redis |
| 前端 | HTML5 + CSS3 + JavaScript |
| 认证 | JWT |
| 部署 | Docker / Render / Vercel |

## 🚀 快速开始

### Docker 运行
```bash
docker build -t forum-v5 .
docker run -p 5000:5000 forum-v5
