from config_test import app, client
from app import db
import json, datetime, pytz
from forms import RegisterForm
from models import User
from flask import (session)

def test_user_login(app, client):
    postObj2 = {'username':'Username', 'password':'Password123'}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'You are now logged in.'
    response3 = client.get('/users/logout')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'You are now logged out.'

def test_user_login_wrong_credentials(app, client):
    postObj2 = {'username':'myusername', 'password':''}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['Wrong credentials.']
    assert result2.get('errors').get('password') == ['This field is required.']

def test_user_login_empty_fields(app, client):
    postObj2 = {'username':'', 'password':''}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['This field is required.']
    assert result2.get('errors').get('password') == ['This field is required.']

def test_user_login_wrong_password(app, client):
    postObj2 = {'username':'Username', 'password':'Passwords123'}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['Wrong password.']