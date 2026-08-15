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


def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'test@example.com'
    })
    data = json.loads(response.data)
    assert response.status_code == 201
    assert 'token' in data
    assert data['username'] == 'testuser'


def test_register_duplicate(client):
    client.post('/api/auth/register', json={
        'username': 'duplicate',
        'password': 'testpass123'
    })
    response = client.post('/api/auth/register', json={
        'username': 'duplicate',
        'password': 'testpass123'
    })
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data


def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'password': 'loginpass123'
    })
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'loginpass123'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'token' in data


def test_login_wrong_password(client):
    client.post('/api/auth/register', json={
        'username': 'wrongpass',
        'password': 'correctpass'
    })
    response = client.post('/api/auth/login', json={
        'username': 'wrongpass',
        'password': 'wrongpass'
    })
    data = json.loads(response.data)
    assert response.status_code == 401
    assert 'error' in data


def test_me_unauthorized(client):
    response = client.get('/api/auth/me')
    data = json.loads(response.data)
    assert response.status_code == 401
    assert 'error' in data
