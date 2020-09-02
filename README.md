# Simple API using Flask

## Demo 
[demo link](https://some-flask-api.herokuapp.com/)

## Endpoints
### Authentication
- Register POST
    - /users/register
- Login POST 
    - /users/login
- Logout GET 
    - /users/logout

### Jobs
- GET 
    - /jobs/ and /jobs/view/[job_id]
    - /jobs/page=[pageNumber] pagination
    - /jobs/sort=[sortKey] sorting
        - sortKeys: 'id', '-id', 'name', '-name', 'description', '-description'
    - /jobs/search=[keyword] searching
- POST 
    - /jobs/
- POST 
    - /jobs/update/[job_id]
- DELETE 
    - /jobs/delete/[job_id]

### Employees
- GET 
    - /employees/ and /employees/view/[employee_id]
    - /employees/page=[pageNumber] pagination
    - /employees/sort=[sortkey] sorting
        - sortKeys: 'id', '-id', 'name', '-name', 'email', '-email'
    - /employees/search=[keyword] searching
- POST 
    - /employees/
- POST 
    - /employees/update/[employee_id]'
- DELETE 
    - /employees/delete/[employee_id]'

## Forms
### User
#### Register new user
- username
- password
- confirm (confirm password)

### Login a user
- username
- password

### Jobs
#### Creating a job
- name
- description

#### Updating / Viewing / Deleting a job
- id
- name
- description


### Employee
#### Creating an employee
- name
- email
- occupations_id

#### Updating / Viewing / Deleting an employee
- id
- name
- email
- occupations_id

# Dev Installation
1. pip install -r requirements.txt 
2. Configure .example_env
3. Rename configured .example_env to .env
4. Create database on postgresql server based on dbname on .env file 
5. python manage.py db init
6. python manage.py db migrate
7. python manage.py db upgrade
8. flask run
9. Use curl or postman or talend api tester on browser

# Testing
1. Create test database on postgres 
2. Configure .env TEST_DATABASE_URL to match test database name
3. rename APP_SETTINGS in .env to config.TestingConfig
4. follow Dev Installation steps 5-7
5. python seeder.py seed
6. python -m pytest
7. python seeder.py unseed