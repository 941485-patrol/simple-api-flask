import os
from os import environ
from flask.cli import FlaskGroup
#from flask_script import Manager
#from flask_migrate import Migrate
from app import app, db

app.config.from_object(environ.get('APP_SETTINGS'))

cli = FlaskGroup(app)

@cli.command('hello')
def say_hello():
    print('hello')

### Command for flask v1.1
#migrate = Migrate(app, db)
#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    #manager.run()
    cli()