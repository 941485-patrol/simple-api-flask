from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation
from tests.user import login, logout

def test_index_not_empty(app, client):
    login(app,client)
    response3 = client.get('/jobs/')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('navi').get('total_items') == 12
    assert len(result3.get('results')) == 5
    assert result3.get('results')[0].get('id') == 1
    response4 = client.get('/jobs/?page=2')
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 200
    assert result4.get('navi').get('total_items') == 12
    assert len(result4.get('results')) == 5
    assert result4.get('results')[2].get('name') == 'name8'
    response5 = client.get('/jobs/?page=3')
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 200
    assert result5.get('navi').get('total_items') == 12
    assert len(result5.get('results')) == 2
    assert result5.get('results')[1].get('name') == 'name12'
    response6 = client.get('/jobs/?page=4')
    assert response6.status_code == 404
    logout(app,client)

def test_index_sorting(app, client):
    login(app,client)
    response = client.get('/jobs/?sort=-id')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('results')[3].get('id') == 9
    assert result.get('results')[3].get('employees')[0].get('name') == 'emp4'
    # response2 = client.get('/jobs/?sort=-employee&page=3')
    # result2 = json.loads(response2.get_data(as_text=True))
    # assert response2.status_code == 200
    # assert result2.get('results')[1].get('employees')[0].get('name') == 'emp1'
    response2 = client.get('/jobs/?search=nam')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('navi').get('total_items') == 12
    assert result2.get('navi').get('items_this_page') == 5
    response3 = client.get('/jobs/?page=2&sort=-description')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('results')[2].get('description') == 'description2'
    response4 = client.get('/jobs/?page=1&sort=-name')
    result4 = json.loads(response4.get_data(as_text=True))
    assert response4.status_code == 200
    assert result4.get('navi').get('total_items') == 12
    assert result4.get('navi').get('items_this_page') == 5
    assert result4.get('results')[4].get('name') == 'name5'
    response5 = client.get('/jobs/?page=2&sort=descriptions')
    result5 = json.loads(response5.get_data(as_text=True))
    assert response5.status_code == 400
    assert result5.get('message') == 'Wrong sorting order.'
    logout(app,client)

def test_index_searching(app, client):
    login(app,client)
    response = client.get('/jobs/?search=name12')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('results')[0].get('name') == 'name12'
    response2 = client.get('/jobs/?search=description12')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('results')[0].get('name') == 'name12'
    response3 = client.get('/jobs/?search=magic5')
    result3 = json.loads(response3.get_data(as_text=True))
    assert response3.status_code == 200
    assert result3.get('message') == 'No data.'
    logout(app,client)

def test_index_search_and_sort(app, client):
    login(app,client)
    response = client.get('/jobs/?search=name&page=1&sort=-name')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('navi').get('items_this_page') == 5
    assert result.get('navi').get('total_items') == 12
    assert result.get('results')[4].get('name') == 'name5'
    response2 = client.get('/jobs/?sort=-name&search=empek')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('message') == 'No data.'
    logout(app,client)

def test_index_notfound(app, client):
    login(app,client)
    response = client.get('/jobs/  ')
    assert response.status_code == 404
    response2 = client.post('/jobs/  ')
    assert response2.status_code == 404
    response3 = client.get('jobs/view/whatisthis')
    assert response3.status_code == 404
    response4 = client.get('jobs/view/')
    assert response4.status_code == 404
    response5 = client.get('jobs/view/  ')
    assert response5.status_code == 404
    response6 = client.get('jobs/view/60')
    assert response6.status_code == 404
    logout(app,client)

def test_create_job(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'Job created.'
    db.session.delete(Occupation.query.filter_by(id=result.get('job_id')).first())
    db.session.commit()
    logout(app,client)

def test_get_job(app, client):
    login(app,client)
    response2 = client.get('/jobs/view/5')
    result2 = json.loads(response2.get_data(as_text=True))
    assert response2.status_code == 200
    assert result2.get('id') == 5
    logout(app,client)

def test_create_job_double_entry(app, client):
    login(app,client)
    postObj1 = {'name': 'name1', 'description':'description2'}
    response1 = client.post('/jobs/', data=postObj1)
    result1 = json.loads(response1.get_data(as_text=True))
    assert response1.status_code == 400
    assert result1.get('errors').get('description') == ['Description is already taken.']
    assert result1.get('errors').get('name') == ['Name is already taken.']
    db.session.commit()
    logout(app,client)

def test_create_job_empty_fields(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': '', 'description':'', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('description') == ['This field is required.']
    assert result.get('errors').get('name') == ['This field is required.']
    logout(app,client)

def test_create_job_incomplete_fields(app, client):
    login(app,client)
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'a', 'description':'abcd', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 400
    assert result.get('errors').get('name') == ['Minimum 2 and maximum 50 characters.']
    assert result.get('errors').get('description') == ['Minimum 5 and maximum 100 characters.']
    logout(app,client)

def test_index_unauthorized(app, client):
    response = client.get('/jobs/')
    assert response.status_code == 401

def test_create_job_unauthorized(app, client):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    postObj = {'name': 'myname', 'description':'mydescription', 'created_at':datenow, 'updated_at':datenow}
    response = client.post('/jobs/', data=postObj)
    assert response.status_code == 401

def test_get_job_unauthorized(app, client):
    response2 = client.get('/jobs/view/11')
    assert response2.status_code == 401