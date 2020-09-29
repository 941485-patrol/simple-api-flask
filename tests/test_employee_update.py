from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee
from tests.user import login,logout

def test_update_get_toupdate_job(app,client):
    login(app,client)
    response = client.get('/jobs/view/6')
    result = json.loads(response.get_data(as_text=True))
    employees = result.get('employees')
    assert response.status_code == 200
    assert len(employees) == 1

def test_update(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':'7', 'name': 'emp77', 'email':'emp77@gmail.com', 'occupations_id':5, 'updated_at':datenow}
    response3 = client.post('/employees/update/7', data=putObj)
    assert response3.status_code == 200
    logout(app,client)

def test_update_again_same_credentials(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    putObj = {'id':'7', 'name': 'emp77', 'email':'emp77@gmail.com', 'occupations_id':5, 'updated_at':datenow}
    response3 = client.post('/employees/update/7', data=putObj)
    assert response3.status_code == 200
    logout(app,client)

def test_update_get_updated_emp(app, client):
    login(app,client)
    response = client.get('/employees/view/7')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('occupations_id') == 5

def test_check_occupation(app, client):
    login(app,client)
    response = client.get('/jobs/view/5')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    employees = result.get('employees')
    found = list(filter(lambda x : x.get('id') == 7 , employees))
    assert len(found) == 1
    logout(app,client)

def test_check_occupation_length(app, client):
    login(app,client)
    response = client.get('/jobs/view/5')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    employees = result.get('employees')
    assert len(employees) == 2
    logout(app,client)

def test_check_null_occupation(app, client):
    login(app, client)
    response = client.get('/jobs/view/6')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    employees = result.get('employees')
    assert employees == []

def test_update_double_entry(app, client):
    login(app,client)
    putObj = {'id':7, 'name': 'emp8', 'email':'emp8@gmail.com', 'occupations_id':5}
    response4 = client.post('/employees/update/7', data=putObj)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('name') == ['Name is already taken.']
    assert result4.get('errors').get('email') == ['E-mail is already taken.']
    logout(app,client)

def test_update_occupations_id_validations(app, client):
    login(app,client)
    putObj = {'id':7, 'name': 'emp77', 'email':'emp77@gmail.com', 'occupations_id':'48'}
    response3 = client.post('/employees/update/7', data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('occupations_id') == ['Wrong Job id.']
    putObj2 = {'id':7, 'name': 'emp77', 'email':'emp77@gmail.com', 'occupations_id':'whatisthis'}
    response4 = client.post('/employees/update/7', data=putObj2)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('occupations_id') == ['Invalid Id number.']
    logout(app,client)

def test_update_id_validations(app, client):
    login(app,client)
    putObj = {'id':'48', 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':'5'}
    response3 = client.post('/employees/update/7', data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('id') == ['Invalid Id path.']
    putObj2 = {'id':'7', 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':'5'}
    response4 = client.post('/employees/update/48', data=putObj2)
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 400
    assert result4.get('errors').get('id') == ['Invalid Id path.']
    putObj3 = {'id':'whatisithis', 'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':'5'}
    response5 = client.post('/employees/update/7', data=putObj3)
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 400
    assert result5.get('errors').get('id') == ['Invalid Id number.']
    logout(app,client)

def test_employee_update_empty_fields(app, client):
    login(app,client)
    putObj = {'id':'', 'name': '', 'email':'', 'occupations_id':''}
    response3 = client.post('/employees/update/7', data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('id') == ['Invalid Id path.']
    assert result3.get('errors').get('email') == ['This field is required.']
    assert result3.get('errors').get('name') == ['This field is required.']
    assert result3.get('errors').get('occupations_id') == ['This field is required.']
    logout(app,client)

def test_employee_update_incomplete_fields(app, client) -> bool : 
    login(app,client)
    putObj = {'id':8, 'name': 'n', 'email':'n', 'occupations_id':'10'}
    response3 = client.post('/employees/update/8', data=putObj)
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('email') == ['Minimum 2 and maximum 50 characters','Invalid Email.']
    assert result3.get('errors').get('name') == ['Minimum 2 and maximum 50 characters']
    logout(app,client)

def test_update_unauthorized(app, client):
    putObj = {'id':7, 'name': 'emp77', 'email':'emp77@gmail.com', 'occupations_id':'5'}
    response3 = client.post('/employees/update/7', data=putObj)
    assert response3.status_code == 401