from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee

def test_update(app, client):
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
    putObj = {'id':result2.get('employee_id'), 'name': 'newEmployeeName', 'email':'newEmployee@gmail.com', 'occupations_id': result.get('job_id')}
    response3 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj)
    assert response3.status_code == 200
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_update_double_entry(app, client):
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
    postObj3 = {'name': 'otheremployeename', 'email':'employee2@gmail.com', 'occupations_id': result.get('job_id')}
    response3 = client.post('/employees/', data=postObj3)
    result3= json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'Employee created.'
    putObj = {'id':result3.get('employee_id'), 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id': result.get('job_id')}
    response4 = client.post('/employees/update/{}'.format(result3.get('employee_id')), data=putObj)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('name') == ['Name is already taken.']
    assert result4.get('errors').get('email') == ['E-mail is already taken.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_update_occupations_id_validations(app, client):
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
    putObj = {'id':result.get('employee_id'), 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':'2'}
    response3 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('occupations_id') == ['Wrong Job id.']
    putObj2 = {'id':result.get('employee_id'), 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':'whatisthis'}
    response4 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj2)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('occupations_id') == ['Invalid Id number.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_update_id_validations(app, client):
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
    putObj = {'id':'2', 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':result.get('job_id')}
    response3 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('id') == ['Invalid Id path.']
    putObj2 = {'id':result.get('job_id'), 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':result.get('job_id')}
    response4 = client.post('/employees/update/2', data=putObj2)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('id') == ['Invalid Id path.']
    putObj3 = {'id':'whatisithis', 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':result.get('job_id')}
    response5 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj3)
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 400
    assert result5.get('errors').get('id') == ['Invalid Id number.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_employee_update_empty_fields(app, client):
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
    putObj = {'id':'', 'name': '', 'email':'', 'occupations_id':''}
    response3 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('id') == ['Invalid Id path.']
    assert result3.get('errors').get('email') == ['This field is required.']
    assert result3.get('errors').get('name') == ['This field is required.']
    assert result3.get('errors').get('occupations_id') == ['This field is required.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()

def test_employee_update_incomplete_fields(app, client) -> bool : 
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
    putObj = {'id':result2.get('employee_id'), 'name': 'n', 'email':'n', 'occupations_id': result.get('job_id')}
    response3 = client.post('/employees/update/{}'.format(result2.get('employee_id')), data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('email') == ['Minimum 2 and maximum 50 characters','Invalid Email.']
    assert result3.get('errors').get('name') == ['Minimum 2 and maximum 50 characters']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()