from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee
from tests.user import login,logout

def test_employee_delete(app, client):
    login(app,client)
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id': result.get('job_id')}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'Employee created.'
    response3 = client.post('/employees/delete/{}'.format(result2.get('employee_id')))
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'Employee deleted.'
    response4 = client.get('/jobs/view/{}'.format(result.get('job_id')))
    result4 = json.loads(response4.get_data(as_text=True))
    assert result4.get('employees') == []
    response5 = client.post('/jobs/delete/{}'.format(result.get('job_id')))
    result5 = json.loads(response5.get_data(as_text=True))
    assert result5.get('message') == 'Job deleted.'
    logout(app,client)

def test_delete_invalid_url(app, client):
    login(app,client)
    response = client.post('/employees/delete/')
    assert response.status_code == 404
    response2 = client.post('/employees/delete/42')
    assert response2.status_code == 404
    response3 = client.post('/employees/delete/    ')
    assert response3.status_code == 404
    response4 = client.post('/employees/delete/whatisithis')
    assert response4.status_code == 404
    logout(app,client)

def test_delete_unauthorized(app,client):
    response3 = client.post('/employees/delete/1')
    assert response3.status_code == 401