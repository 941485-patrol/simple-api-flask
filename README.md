1. pip install -r requirements.txt 
2. Configure .example_env
3. Rename configured .example_env to .env
4. Create database on postgresql server based on dbname on .env file 
5. python manage.py db init
6. python manage.py db migrate
7. python manage.py db upgrade
8. flask run
9. Use curl or postman
