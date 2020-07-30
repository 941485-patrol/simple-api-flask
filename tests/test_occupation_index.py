from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation
from tests.user import login, logout

def test_index_empty(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    response = client.get('/jobs/')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'No data.'
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_index_not_empty(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': 'myname1', 'description':'mydescription1', 'created_at':datenow, 'updated_at':datenow}
    response2 = client.post('/jobs/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'Job created.'
    response3 = client.get('/jobs/')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('navi').get('total_items') == 2
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_index_notfound(app, client):
    login(app,client)
    response = client.get('/jobs/  ')
    assert response.status_code == 404
    response2 = client.post('/jobs/  ')
    assert response2.status_code == 404
    response3 = client.get('jobs/view/whatisthis')
    assert response3.status_code == 404
    response4 = client.get('jobs/view/')
    assert response4.status_code == 404
    response5 = client.get('jobs/view/  ')
    assert response5.status_code == 404
    response6 = client.get('jobs/view/2')
    assert response6.status_code == 404
    logout(app,client)

def test_create_job(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_get_job(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    response2 = client.get('/jobs/view/{}'.format(result.get('job_id')))
    result2 = json.loads(response2.get_data(as_text=True))
    assert response.status_code == 200
    assert result2.get('id') == result.get('job_id')
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_job_double_entry(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj1 = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response1 = client.post('/jobs/', data=postObj1)
    result1 = json.loads(response1.get_data(as_text=True))
    assert response1.status_code == 400
    assert result1.get('errors').get('description') == ['Description is already taken.']
    assert result1.get('errors').get('name') == ['Name is already taken.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_job_empty_fields(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': '', 'description':'', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('description') == ['This field is required.']
    assert result.get('errors').get('name') == ['This field is required.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_job_incomplete_fields(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'a', 'description':'abcd', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('name') == ['Minimum 2 and maximum 50 characters.']
    assert result.get('errors').get('description') == ['Minimum 5 and maximum 100 characters.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_index_unauthorized(app, client):
    db.session.query(Occupation).delete()
    db.session.commit()
    response = client.get('/jobs/')
    assert response.status_code == 401
    db.session.query(Occupation).delete()
    db.session.commit()

def test_create_job_unauthorized(app, client):
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    assert response.status_code == 401
    db.session.query(Occupation).delete()
    db.session.commit()

def test_get_job_unauthorized(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    logout(app,client)
    response2 = client.get('/jobs/view/{}'.format(result.get('job_id')))
    assert response2.status_code == 401
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)