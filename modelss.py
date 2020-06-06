# Backup Model file
from app import db
class Occupation(db.Model):
    __tablename__ = 'occupations'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True)
    description=db.Column(db.String(100))
    created_at=db.Column(db.DateTime(timezone=True))
    updated_at=db.Column(db.DateTime(timezone=True))
    employees=db.relationship('Employee', backref='occupation', lazy=True)

    def __init__(self, name, description, created_at, updated_at, employees):
        self.name = name
        self.created_at = created_at
        self.description = description
        self.updated_at = updated_at
        self.employees = employees

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Employee(db.Model):
    __tablename__ = 'employees'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    created_at=db.Column(db.DateTime(timezone=True))
    updated_at=db.Column(db.DateTime(timezone=True))
    occupations_id=db.Column(db.Integer, db.ForeignKey('occupation.id'))

    def __init__(self, name, email, created_at, updated_at, occupations_id):
        self.name = name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.occupations_id = occupations_id
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'occupations_id':self.occupations_id,
        }
