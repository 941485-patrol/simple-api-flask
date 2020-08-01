# Simple API using Flask

## Demo 
[demo link](http://some-flask-api.herokuapp.com/)

## Endpoints
Jobs
    GET - /jobs/ and /jobs/view/'job_id'
    POST - /jobs/
    POST - /jobs/update/'job_id'
    DELETE - /jobs/delete/'job_id'

Employees
    GET - /employees/ and /employees/view/'employee_id'
    POST - /employees/
    POST - /employees/update/'employee_id'
    DELETE - /employees/delete/'employee_id'

## Forms

### Jobs
#### Creating a job
1. name
2. description

#### Updating / Viewing / Deleting a job
1. id
2. name
3. description

### Employee
#### Creating an employee
1. name
2. email
3. occupations_id

#### Updating / Viewing / Deleting an employee
1. id
2. name
3. email
4. occupations_id

# Dev Installation
1. pip install -r requirements.txt 
2. Configure .example_env
3. Rename configured .example_env to .env
4. Create database on postgresql server based on dbname on .env file 
5. python manage.py db init
6. python manage.py db migrate
7. python manage.py db upgrade
8. flask run
9. Use curl or postman

# Testing
1. Create test database on postgres 
2. Configure .env TEST_DATABASE_URL to match test database name
3. rename APP_SETTINGS in .env to config.TestingConfig
4. follow Dev Installation steps 5-7
5. python -m pytest