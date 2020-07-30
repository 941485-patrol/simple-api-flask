from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee
from tests.user import login,logout

def test_index_empty(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    response = client.get('/employees/')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'No data.'
    db.session.query(Employee).delete()
    db.session.commit()
    logout(app,client)

def test_index_not_empty(app, client):
    login(app,client)
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
    postObj3 = {'name': 'employeename1', 'email':'employee2@gmail.com', 'occupations_id': result.get('job_id')}
    response3 = client.post('/employees/', data=postObj3)
    result3= json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'Employee created.'
    response4 = client.get('/employees/')
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 200
    assert result4.get('navi').get('total_items') == 2
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_index_notfound(app, client):
    login(app,client)
    response = client.get('/employees/  ')
    assert response.status_code == 404
    response2 = client.post('/employees/  ')
    assert response2.status_code == 404
    response3 = client.get('employees/view/whatisthis')
    assert response3.status_code == 404
    response4 = client.get('employees/view/')
    assert response4.status_code == 404
    response5 = client.get('employees/view/  ')
    assert response5.status_code == 404
    response6 = client.get('employees/view/2')
    assert response6.status_code == 404
    logout(app,client)

def test_create_employee(app, client):
    login(app,client)
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
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_get_employee(app, client):
    login(app,client)
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
    response3 = client.get('/employees/view/{}'.format(result2.get('employee_id')))
    result3 = json.loads(response3.get_data(as_text=True))
    assert result3.get('id') == result2.get('employee_id')
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_employee_double_entry(app, client):
    login(app,client)
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
    postObj3 = {'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id': result.get('job_id')}
    response3 = client.post('/employees/', data=postObj3)
    result3= json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('email') == ['E-mail is already taken.']
    assert result3.get('errors').get('name') == ['Name is already taken.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_employee_empty_fields(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': '', 'email':'', 'occupations_id':''}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['This field is required.']
    assert result2.get('errors').get('name') == ['This field is required.']
    assert result2.get('errors').get('occupations_id') == ['This field is required.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_employee_incomplete_fields(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': 'a', 'email':'a', 'occupations_id':''}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['Minimum 2 and maximum 50 characters','Invalid Email.']
    assert result2.get('errors').get('name') == ['Minimum 2 and maximum 50 characters']
    assert result2.get('errors').get('occupations_id') == ['This field is required.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_employee_invalid_email(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': 'employeeName', 'email':'j@j', 'occupations_id':result.get('job_id')}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['Invalid Email.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_create_employee_occupations_id_validations(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    postObj2 = {'name': 'employeeName', 'email':'employee1@gmail.com', 'occupations_id':'2'}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('occupations_id') == ['Wrong Job id.']
    postObj3 = {'name': 'employeeName', 'email':'employee1@gmail.com', 'occupations_id':'WHAT'}
    response3 = client.post('/employees/', data=postObj3)
    result3= json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('occupations_id') == ['Invalid Id number.']
    postObj4 = {'name': 'employeeName', 'email':'employee1@gmail.com', 'occupations_id':'0'}
    response4 = client.post('/employees/', data=postObj4)
    result4= json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('occupations_id') == ['Invalid Id number.']
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_get_employees_unauthorized(app,client):
    db.session.query(Employee).delete()
    db.session.commit()
    response = client.get('/employees/')
    assert response.status_code == 401
    db.session.query(Employee).delete()
    db.session.commit()

def test_create_employee_unauthorized(app, client):
    login(app,client)
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    postObj = {'name': 'myname', 'description':'mydescription'}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    logout(app,client)
    postObj2 = {'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id': result.get('job_id')}
    response2 = client.post('/employees/', data=postObj2)
    assert response2.status_code == 401
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)

def test_get_employee_unauthorized(app, client):
    login(app,client)
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
    logout(app,client)
    response3 = client.get('/employees/view/{}'.format(result2.get('employee_id')))
    assert response3.status_code == 401
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    logout(app,client)