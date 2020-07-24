from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation

def test_index_empty(app, client):
    db.session.query(Occupation).delete()
    db.session.commit()
    response = client.get('/jobs/')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'No data.'
    db.session.query(Occupation).delete()
    db.session.commit()

def test_index_not_empty(app, client):
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

def test_index_notfound(app, client):
    response = client.get('/jobs/  ')
    assert response.status_code == 404
    response2 = client.post('/jobs/  ')
    assert response2.status_code == 404

def test_create_job(app, client):
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

def test_create_job_empty_fields(app, client):
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