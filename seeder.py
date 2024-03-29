from app import app, db
from os import environ
from models import User , Occupation, Employee
from werkzeug.security import generate_password_hash
from flask.cli import FlaskGroup
import pytz
import datetime
import click

app.config.from_object(environ.get('APP_SETTINGS'))

cli = FlaskGroup(app)

# @click.group()
# def cli():
#     pass

# @cli.command()
# def seedUser():
#     timezone=pytz.timezone('UTC')
#     datenow = timezone.localize(datetime.datetime.utcnow())
#     hashed_pass = generate_password_hash('Password123',method="pbkdf2:sha256", salt_length=8)
#     usr=User(username='Username', password=hashed_pass, created_at=datenow, updated_at=datenow)
#     db.session.add(usr)
#     db.session.commit()
#     click.echo('User created.')

# @cli.command()
# def unseedUser():
#     db.session.query(User).delete()
#     db.session.commit()
#     click.echo('User deleted')

@cli.command()
def seed():
    db.create_all()
    click.echo('Database created')
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    hashed_pass = generate_password_hash('Password123',method="pbkdf2:sha256", salt_length=8)
    usr=User(username='Username', password=hashed_pass, created_at=datenow, updated_at=datenow)
    db.session.add(usr)
    db.session.commit()
    click.echo('User created.')
    j1=Occupation(name='name1', description='description1', created_at=datenow, updated_at=datenow)
    j2=Occupation(name='name2', description='description2', created_at=datenow, updated_at=datenow)
    j3=Occupation(name='name3', description='description3', created_at=datenow, updated_at=datenow)
    j4=Occupation(name='name4', description='description4', created_at=datenow, updated_at=datenow)
    j5=Occupation(name='name5', description='description5', created_at=datenow, updated_at=datenow)
    j6=Occupation(name='name6', description='description6', created_at=datenow, updated_at=datenow)
    j7=Occupation(name='name7', description='description7', created_at=datenow, updated_at=datenow)
    j8=Occupation(name='name8', description='description8', created_at=datenow, updated_at=datenow)
    j9=Occupation(name='name9', description='description9', created_at=datenow, updated_at=datenow)
    j10=Occupation(name='name10', description='description10', created_at=datenow, updated_at=datenow)
    j11=Occupation(name='name11', description='description11', created_at=datenow, updated_at=datenow)
    j12=Occupation(name='name12', description='description12', created_at=datenow, updated_at=datenow)
    db.session.add(j1)
    db.session.add(j2)
    db.session.add(j3)    
    db.session.add(j4)    
    db.session.add(j5)
    db.session.add(j6)    
    db.session.add(j7)
    db.session.add(j8)
    db.session.add(j9)
    db.session.add(j10)
    db.session.add(j11)
    db.session.add(j12)
    db.session.flush()
    db.session.commit()
    click.echo('Job table created')
    e1 = Employee(name='emp1', email='emp1@gmail.com', occupations_id=j12.id, created_at=datenow, updated_at=datenow)
    e2 = Employee(name='emp2', email='emp2@gmail.com', occupations_id=j11.id, created_at=datenow, updated_at=datenow)
    e3 = Employee(name='emp3', email='emp3@gmail.com', occupations_id=j10.id, created_at=datenow, updated_at=datenow)
    e4 = Employee(name='emp4', email='emp4@gmail.com', occupations_id=j9.id, created_at=datenow, updated_at=datenow)
    e5 = Employee(name='emp5', email='emp5@gmail.com', occupations_id=j8.id, created_at=datenow, updated_at=datenow)
    e6 = Employee(name='emp6', email='emp6@gmail.com', occupations_id=j7.id, created_at=datenow, updated_at=datenow)
    e7 = Employee(name='emp7', email='emp7@gmail.com', occupations_id=j6.id, created_at=datenow, updated_at=datenow)
    e8 = Employee(name='emp8', email='emp8@gmail.com', occupations_id=j5.id, created_at=datenow, updated_at=datenow)
    e9 = Employee(name='emp9', email='emp9@gmail.com', occupations_id=j4.id, created_at=datenow, updated_at=datenow)
    e10 = Employee(name='emp10', email='emp10@gmail.com', occupations_id=j3.id, created_at=datenow, updated_at=datenow)
    e11 = Employee(name='emp11', email='emp11@gmail.com', occupations_id=j2.id, created_at=datenow, updated_at=datenow)
    e12 = Employee(name='emp12', email='emp12@gmail.com', occupations_id=j1.id, created_at=datenow, updated_at=datenow)
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)    
    db.session.add(e4)    
    db.session.add(e5)
    db.session.add(e6)    
    db.session.add(e7)
    db.session.add(e8)
    db.session.add(e9)
    db.session.add(e10)
    db.session.add(e11)
    db.session.add(e12)
    db.session.flush()
    db.session.commit()
    click.echo('Employee table created')

@cli.command()
def unseed():
    db.session.query(User).delete()
    db.session.commit()
    click.echo('Users table deleted')
    db.session.query(Employee).delete()
    db.session.commit()
    click.echo('Employees table deleted')
    db.session.query(Occupation).delete()
    db.session.commit()
    click.echo('Occupations table deleted')
    db.drop_all()
    click.echo('Database dropped')

if __name__ == '__main__':
    cli()