from config_test import app, client
from app import db
import json, datetime, pytz
from forms import JobForm
from models import Occupation, Employee
from tests.user import login, logout

def test_job_index_empty(app, client):
    db.session.query(Employee).delete()
    db.session.commit()
    db.session.query(Occupation).delete()
    db.session.commit()
    login(app,client)
    response = client.get('/jobs/')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'No data.'
    logout(app,client)

def test_employee_index_empty(app, client):
    login(app,client)
    response = client.get('/employees/')
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result.get('message') == 'No data.'
    logout(app,client)