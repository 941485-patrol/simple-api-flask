from config_test import app, client
from app import db
import json, datetime, pytz
from forms import RegisterForm
from models import User
from flask import (session)

def test_user_login(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'Mypassword123'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'User created.'
    postObj2 = {'username':'myusername', 'password':'Mypassword123'}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'You are now logged in.'
    response3 = client.get('/users/logout')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'You are now logged out.'
    db.session.query(User).delete()
    db.session.commit()

def test_user_login_wrong_credentials(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'Mypassword123'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'User created.'
    postObj2 = {'username':'myusername', 'password':''}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['Wrong credentials.']
    assert result2.get('errors').get('password') == ['This field is required.']
    response3 = client.get('/users/logout')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'You are now logged out.'
    db.session.query(User).delete()
    db.session.commit()

def test_user_login_empty_fields(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'Mypassword123'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'User created.'
    postObj2 = {'username':'', 'password':''}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['This field is required.']
    assert result2.get('errors').get('password') == ['This field is required.']
    response3 = client.get('/users/logout')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'You are now logged out.'
    db.session.query(User).delete()
    db.session.commit()

def test_user_login_wrong_password(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'Mypassword123'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'User created.'
    postObj2 = {'username':'myusername', 'password':'mypassword123'}
    response2 = client.post('/users/login', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('username') == ['Wrong password.']
    response3 = client.get('/users/logout')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'You are now logged out.'
    db.session.query(User).delete()
    db.session.commit()