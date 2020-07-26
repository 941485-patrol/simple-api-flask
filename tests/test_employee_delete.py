from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee

def test_delete(app, client):
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
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
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_delete_invalid_url(app, client):
    response = client.post('/employees/delete/')
    assert response.status_code == 404
    response2 = client.post('/employees/delete/2')
    assert response2.status_code == 404
    response3 = client.post('/employees/delete/    ')
    assert response3.status_code == 404
    response4 = client.post('/employees/delete/whatisithis')
    assert response4.status_code == 404