from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation
from tests.user import login, logout

def test_update_occupation(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result.get('job_id'), 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result.get('job_id')), data=putObj)
    assert response2.status_code == 200
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_invalid_id_number(app, client):
    login(app,client)
    # Id is not a number
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': 'abc', 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result.get('job_id')), data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Invalid Id number.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_wrong_job_id(app, client):
    # New job_id is supposed to be 1 and not 2.
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':'2', 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/2', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Wrong Job id.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_invalid_id_path(app, client):
    # Id url path is invalid because job_id 2 does not exist yet.
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':result.get('job_id'), 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/2', data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('id') == ['Invalid Id path.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_invalid_url(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result.get('job_id'), 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/invalid_url', data=putObj)
    assert response2.status_code == 404
    response3 = client.post('/jobs/update/', data=putObj)
    assert response3.status_code == 404
    response4 = client.post('/jobs/update/   ', data=putObj)
    assert response4.status_code == 404
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_empty_fields(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result.get('job_id'), 'name': '', 'description':'', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result.get('job_id')), data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('description') == ['This field is required.']
    assert result2.get('errors').get('name') == ['This field is required.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_incomplete_fields(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result.get('job_id'), 'name': 'a', 'description':'abcd', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result.get('job_id')), data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('name') == ['Minimum 2 and maximum 50 characters.']
    assert result2.get('errors').get('description') == ['Minimum 5 and maximum 100 characters.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_double_entry(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    assert response.status_code == 200

    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj1 = {'name': 'myothername', 'description':'myotherdesc', 'created_at':datenow, 'updated_at':datenow}
    response1 = client.post('/jobs/', data=postObj1)
    result1 = json.loads(response1.get_data(as_text=True))
    assert response1.status_code == 200
    
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result1.get('job_id'), 'name': 'myname', 'description':'mydescription', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result1.get('job_id')), data=putObj)
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('description') == ['Description is already taken.']
    assert result2.get('errors').get('name') == ['Name is already taken.']
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_update_occupation_unauthorized(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    logout(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id': result.get('job_id'), 'name': 'myname1', 'description':'mydescription1', 'updated_at':datenow}
    response2 = client.post('/jobs/update/{}'.format(result.get('job_id')), data=putObj)
    assert response2.status_code == 401
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)