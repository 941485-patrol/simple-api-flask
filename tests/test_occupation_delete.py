from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation
from tests.user import login, logout

def test_delete(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    response2 = client.post('/jobs/delete/{}'.format(result.get('job_id')))
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'Job deleted.'
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_delete_invalid_url(app, client):
    login(app,client)
    db.session.query(Occupation).delete()
    db.session.commit()
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    assert response.status_code == 200
    response2 = client.post('/jobs/delete/  ')
    assert response2.status_code == 404
    response3 = client.post('/jobs/delete/supposedtobeoccid')
    assert response3.status_code == 404
    response4 = client.post('/jobs/delete/')
    assert response4.status_code == 404
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_delete_unauthorized(app, client):
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
    response2 = client.post('/jobs/delete/{}'.format(result.get('job_id')))
    assert response2.status_code == 401
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)