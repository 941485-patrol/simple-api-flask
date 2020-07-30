from config_test import app, client
from app import db
import json, datetime, pytz
from forms import RegisterForm
from models import User

def test_user_logout(app, client):
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