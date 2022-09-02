#### Flask API using Flask-SQLAlchemy, Flask-WTForms and PostgreSQL.
### Demo
https://some-flask-api.herokuapp.com \
username: Username \
password: Password123 \
*Note: Use [Talend](https://chrome.google.com/webstore/detail/talend-api-tester-free-ed/aejoelaoggembcahagimdiliamlcdmfm?hl=en) or [Postman](https://www.postman.com/) to open the website.
### Instructions
#### Dev Installation
1. pip install -r requirements.txt 
2. Configure .example_env
3. Rename configured .example_env to .env
4. Create database on postgresql server based on dbname on .env file 
5. flask db init
6. flask db migrate
7. flask db upgrade
8. python seeder.py seed
9. flask run
10. Use curl or postman or talend api tester on browser

#### Testing
1. Create test database on postgres 
2. Configure .env TEST_DATABASE_URL to match test database name
3. rename APP_SETTINGS in .env to config.TestingConfig
4. follow Dev Installation steps 5-7
5. python seeder.py seed
6. python -m pytest
7. python seeder.py unseed

*Note: Be sure to run postgresql server and create a database before cloning. \
*Test notes: Be sure to follow testing steps before testing again. 

### Docker (If you want to run the site using docker)
1. Configure .example_env and .example_database_env
2. Rename to .env and database.env
1. docker-compose up
2. docker-compose run postgres bash
3. psql --host=postgres --username=POSTGRES_USER
4. c\ POSTGRES_DB then exit
5. docker-compose run some-flask-api python seeder.py seed
5. docker-compose run some-flask-api (testing steps 6-7 if you want to test application)
10. Use curl or postman or talend api tester on browser

### Endpoints
|Method|URL|Form|Description|
|------|---|----|-----------|
|POST|/users/register|[username][password][confirm]|Register a user.
|POST|/users/login|[username][password]|Log in a user.
|GET|/users/logout|None|Log out a user.
|GET|/jobs/|None|Get all jobs.
|POST|/jobs/|[name][description]|Create a job.
|GET|/jobs/view/:id|None|Get job by id.
|POST|/jobs/update/:id|[id][name][description]|Update a job.
|DELETE|/jobs/delete/:id|None|Delete an animal.
|GET|/employees/|None|Get all employees.
|POST|/employees/|[name][email][occupations_id]|Create an employee.
|GET|/employees/view/:id|None|Get an employee by id.
|POST|/employees/update/:id|[id][name][email][occupations_id]|Update an employee.
|DELETE|/employees/delete/:id|None|Delete an employee.

### Query strings
|Parameter|Description|
|---------|-----------|
|sort|Sort by [id], [name], [description (job only] or [email (employee only)]. Add "-" for descending order.|
|search|Search by [name][description][email].|
|page|Page number.|