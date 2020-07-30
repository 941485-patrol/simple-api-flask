from config_test import app, client
from app import db
import json, datetime, pytz
from forms import RegisterForm
from models import User

def test_register(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'Mypassword123'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'User created.'
    db.session.query(User).delete()
    db.session.commit()

def test_register_empty_fields(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': '', 'password':'', 'confirm':''}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('username') == ['This field is required.']
    assert result.get('errors').get('password') == ['This field is required.']
    assert result.get('errors').get('confirm') == ['This field is required.']
    db.session.query(User).delete()
    db.session.commit()

def test_register_incomplete_fields(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'user', 'password':'Pass12', 'confirm':'Pass12'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('username') == ['Username must be between 8 and 16 characters.']
    assert result.get('errors').get('password') == ['Password must be between 8 and 16 characters.']
    db.session.query(User).delete()
    db.session.commit()

def test_register_password_must_match(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'Mypassword123', 'confirm':'MYpassword321'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('password') == ['Passwords must match.']
    postObj2 = {'username': 'myusername', 'password':'Mypas1', 'confirm':'Mypas2'}
    response2 = client.post('/users/register', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result.get('errors').get('password') == ['Passwords must match.']
    db.session.query(User).delete()
    db.session.commit()

def test_register_invalid_password(app, client):
    db.session.query(User).delete()
    db.session.commit()
    postObj = {'username': 'myusername', 'password':'mypassword', 'confirm':'mypassword'}
    response = client.post('/users/register', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('password') == ['Password must contain at least one number and a capital letter.']
    postObj2 = {'username': 'myusername', 'password':'mypassword', 'confirm':'Mypassword123'}
    response2 = client.post('/users/register', data=postObj2)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('password') == [
        'Passwords must match.',
        'Password must contain at least one number and a capital letter.',]
    db.session.query(User).delete()
    db.session.commit()