from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation
from tests.user import login, logout

def test_update_occupation(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': 7, 'name': 'name77', 'description':'description77', 'updated_at':datenow}
    response2 = client.post('/jobs/update/7', data=putObj)
    assert response2.status_code == 200
    logout(app,client)

def test_update_occupation_invalid_id_number(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': 'abc', 'name': 'name7', 'description':'description7', 'updated_at':datenow}
    response2 = client.post('/jobs/update/7', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Invalid Id number.']
    logout(app,client)

def test_update_occupation_wrong_job_id(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':'22', 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/22', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Wrong Job id.']
    logout(app,client)

def test_update_occupation_invalid_id_path(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':7, 'name': 'name7', 'description':'description7', 'updated_at':datenow}
    response2 = client.post('/jobs/update/2', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Invalid Id path.']
    logout(app,client)

def test_update_occupation_invalid_url(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':7, 'name': 'name7', 'description':'description7', 'updated_at':datenow}
    response2 = client.post('/jobs/update/invalid_url', data=putObj)
    assert response2.status_code == 404
    response3 = client.post('/jobs/update/', data=putObj)
    assert response3.status_code == 404
    response4 = client.post('/jobs/update/   ', data=putObj)
    assert response4.status_code == 404
    logout(app,client)

def test_update_occupation_empty_fields(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': 7, 'name': '', 'description':'', 'updated_at':datenow}
    response2 = client.post('/jobs/update/7', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('description') == ['This field is required.']
    assert result2.get('errors').get('name') == ['This field is required.']
    logout(app,client)

def test_update_occupation_incomplete_fields(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': 7, 'name': 'a', 'description':'abcd', 'updated_at':datenow}
    response2 = client.post('/jobs/update/7', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('name') == ['Minimum 2 and maximum 50 characters.']
    assert result2.get('errors').get('description') == ['Minimum 5 and maximum 100 characters.']
    logout(app,client)

def test_update_occupation_double_entry(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':8, 'name': 'name77', 'description':'description77', 'updated_at':datenow}
    response2 = client.post('/jobs/update/8', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('description') == ['Description is already taken.']
    assert result2.get('errors').get('name') == ['Name is already taken.']
    logout(app,client)

def test_update_occupation_unauthorized(app, client):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':7, 'name': 'name7', 'description':'description7', 'updated_at':datenow}
    response2 = client.post('/jobs/update/7', data=putObj)
    assert response2.status_code == 401