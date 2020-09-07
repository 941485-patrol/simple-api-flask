from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import User

def login(app, client):
    logObj = {'username':'Username', 'password':'Password123'}
    resp2 = client.post('/users/login', data=logObj)
    res2 = json.loads(resp2.get_data(as_text=True))
    assert resp2.status_code == 200
    assert res2.get('message') == 'You are now logged in.'

def logout(app, client):
    resp = client.get('/users/logout')
    res = json.loads(resp.get_data(as_text=True))
    assert resp.status_code == 200
    assert res.get('message') == 'You are now logged out.'