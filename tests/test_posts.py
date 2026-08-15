#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from app import create_app


@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def get_token(client):
    client.post('/api/auth/register', json={
        'username': 'postuser',
        'password': 'postpass123'
    })
    response = client.post('/api/auth/login', json={
        'username': 'postuser',
        'password': 'postpass123'
    })
    data = json.loads(response.data)
    return data['token']


def test_create_post(client):
    token = get_token(client)
    response = client.post('/api/posts', json={
        'title': '测试帖子',
        'content': '这是测试内容'
    }, headers={'Authorization': f'Bearer {token}'})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['title'] == '测试帖子'


def test_create_post_unauthorized(client):
    response = client.post('/api/posts', json={
        'title': '测试帖子',
        'content': '这是测试内容'
    })
    data = json.loads(response.data)
    assert response.status_code == 401


def test_get_posts(client):
    token = get_token(client)
    client.post('/api/posts', json={
        'title': '帖子1',
        'content': '内容1'
    }, headers={'Authorization': f'Bearer {token}'})
    client.post('/api/posts', json={
        'title': '帖子2',
        'content': '内容2'
    }, headers={'Authorization': f'Bearer {token}'})

    response = client.get('/api/posts')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data['data']) >= 2


def test_get_post_detail(client):
    token = get_token(client)
    response = client.post('/api/posts', json={
        'title': '详情测试',
        'content': '详情内容'
    }, headers={'Authorization': f'Bearer {token}'})
    data = json.loads(response.data)
    post_id = data['id']

    response = client.get(f'/api/posts/{post_id}')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['title'] == '详情测试'


def test_delete_post(client):
    token = get_token(client)
    response = client.post('/api/posts', json={
        'title': '删除测试',
        'content': '删除内容'
    }, headers={'Authorization': f'Bearer {token}'})
    data = json.loads(response.data)
    post_id = data['id']

    response = client.delete(f'/api/posts/{post_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = client.get(f'/api/posts/{post_id}')
    data = json.loads(response.data)
    assert response.status_code == 404
