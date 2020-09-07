from config_test import app, client
from app import db
import json, datetime, pytz
from models import Occupation, Employee
from tests.user import login,logout

def test_index_not_empty(app, client):
    login(app,client)
    response4 = client.get('/employees/')
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 200
    assert result4.get('navi').get('total_items') == 12
    assert len(result4.get('results')) == 5
    assert result4.get('results')[0].get('id') == 1
    response5 = client.get('/employees/?page=2')
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 200
    assert result5.get('navi').get('total_items') == 12
    assert len(result5.get('results')) == 5
    assert result5.get('results')[0].get('id') == 6
    response6 = client.get('/employees/?page=3')
    result6 = json.loads(response6.get_data(as_text=True))
    assert response6.status_code == 200
    assert result6.get('navi').get('total_items') == 12
    assert len(result6.get('results')) == 2
    assert result6.get('results')[0].get('id') == 11
    response7 = client.get('/employees/?page=4')
    assert response7.status_code == 404
    logout(app,client)

def test_index_sorting(app, client):
    login(app,client)
    response = client.get('/employees/?sort=-id')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('results')[3].get('id') == 9
    assert result.get('results')[3].get('occupation').get('occupations_name') == 'name4'
    # response2 = client.get('/employees/?sort=-job&page=3')
    # result2 = json.loads(response2.get_data(as_text=True))
    # assert response2.status_code == 200
    # assert result2.get('results')[1].get('occupation').get('occupations_name') == 'name1'
    response3 = client.get('/employees/?page=2&sort=email')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('results')[2].get('email') == 'emp5@gmail.com'
    response4 = client.get('/employees/?page=1&sort=-name')
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 200
    assert result4.get('results')[4].get('name') == 'emp5'
    response5 = client.get('/employees/?page=2&sort=emails')
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 400
    assert result5.get('message') == 'Wrong sorting order.'
    logout(app,client)

def test_index_searching(app, client):
    login(app,client)
    response = client.get('/employees/?search=emp12')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('results')[0].get('name') == 'emp12'
    response2 = client.get('/employees/?search=description12')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('results')[0].get('name') == 'emp1'
    response2 = client.get('/employees/?search=em')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('navi').get('total_items') == 12
    assert result2.get('navi').get('items_this_page') == 5
    response3 = client.get('/employees/?search=magic5')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'No data.'
    logout(app,client)

def test_index_search_and_sort(app, client):
    login(app,client)
    response = client.get('/employees/?search=emp&page=1&sort=-name')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('navi').get('items_this_page') == 5
    assert result.get('results')[4].get('name') == 'emp5'
    response2 = client.get('/employees/?sort=-name&search=empk')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'No data.'
    response3 = client.get('/employees/?search=description&page=1&sort=-name')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('navi').get('items_this_page') == 5
    assert result3.get('navi').get('total_items') == 12
    assert result3.get('results')[4].get('name') == 'emp5'
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
    response6 = client.get('employees/view/42')
    assert response6.status_code == 404
    logout(app,client)

def test_create_employee(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj2 = {'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id':5, 'created_at':datenow, 'updated_at':datenow}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'Employee created.'
    db.session.delete(Employee.query.filter_by(id=result2.get('employee_id')).first())
    db.session.commit()
    logout(app,client)

def test_get_employee(app, client):
    login(app,client)
    response3 = client.get('/employees/view/7')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('id') == 7
    logout(app,client)

def test_create_employee_double_entry(app, client):
    login(app,client)
    postObj3 = {'name': 'emp1', 'email':'emp2@gmail.com', 'occupations_id':5}
    response3 = client.post('/employees/', data=postObj3)
    result3= json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 400
    assert result3.get('errors').get('email') == ['E-mail is already taken.']
    assert result3.get('errors').get('name') == ['Name is already taken.']
    logout(app,client)

def test_create_employee_empty_fields(app, client):
    login(app,client)
    postObj2 = {'name': '', 'email':'', 'occupations_id':''}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['This field is required.']
    assert result2.get('errors').get('name') == ['This field is required.']
    assert result2.get('errors').get('occupations_id') == ['This field is required.']
    logout(app,client)

def test_create_employee_incomplete_fields(app, client):
    login(app,client)
    postObj2 = {'name': 'a', 'email':'a', 'occupations_id':''}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['Minimum 2 and maximum 50 characters','Invalid Email.']
    assert result2.get('errors').get('name') == ['Minimum 2 and maximum 50 characters']
    assert result2.get('errors').get('occupations_id') == ['This field is required.']
    logout(app,client)

def test_create_employee_invalid_email(app, client):
    login(app,client)
    postObj2 = {'name': 'employeeName', 'email':'j@j', 'occupations_id':5}
    response2 = client.post('/employees/', data=postObj2)
    result2= json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 400
    assert result2.get('errors').get('email') == ['Invalid Email.']
    logout(app,client)

def test_create_employee_occupations_id_validations(app, client):
    login(app,client)
    postObj2 = {'name': 'employeeName', 'email':'employee1@gmail.com', 'occupations_id':'48'}
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
    logout(app,client)

def test_get_employees_unauthorized(app,client):
    response = client.get('/employees/')
    assert response.status_code == 401

def test_create_employee_unauthorized(app, client):
    postObj2 = {'name': 'employeename', 'email':'employee1@gmail.com', 'occupations_id': 5}
    response2 = client.post('/employees/', data=postObj2)
    assert response2.status_code == 401

def test_get_employee_unauthorized(app, client):
    response3 = client.get('/employees/view/2')
    assert response3.status_code == 401