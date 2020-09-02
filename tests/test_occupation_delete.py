from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation
from tests.user import login, logout

def test_job_delete(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    putObj = {'id':'1', 'name':'emp1', 'email':'emp1@gmail.com','occupations_id':result.get('job_id'),'updated_at':datenow}
    responsePut = client.post('/employees/update/1', data=putObj)
    assert responsePut.status_code == 200
    response2 = client.post('/jobs/delete/{}'.format(result.get('job_id')))
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'Job deleted.'
    responsePutGet = client.get('/employees/view/1')
    resultPutGet = json.loads(responsePutGet.get_data(as_text=True))
    assert resultPutGet.get('occupation') == None
    putObj2 = {'id':'1', 'name':'emp1', 'email':'emp1@gmail.com','occupations_id':12,'updated_at':datenow}
    responsePut2 = client.post('/employees/update/1', data=putObj2)
    assert responsePut2.status_code == 200
    response3 = client.get('/employees/view/1')
    result3 = json.loads(response3.get_data(as_text=True))
    assert result3.get('occupations_id') == 12
    logout(app,client)

def test_delete_invalid_url(app, client):
    login(app,client)
    response2 = client.post('/jobs/delete/  ')
    assert response2.status_code == 404
    response3 = client.post('/jobs/delete/supposedtobeoccid')
    assert response3.status_code == 404
    response4 = client.post('/jobs/delete/')
    assert response4.status_code == 404
    logout(app,client)

def test_delete_unauthorized(app, client):
    response2 = client.post('/jobs/delete/5')
    assert response2.status_code == 401
    logout(app,client)