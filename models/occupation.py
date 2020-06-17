from app import db
from flask import jsonify
class Occupation(db.Model):
    __tablename__ = 'occupations'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True)
    description=db.Column(db.String(100))
    created_at=db.Column(db.DateTime(timezone=True))
    updated_at=db.Column(db.DateTime(timezone=True))
    employees=db.relationship('Employee', lazy='select', backref=db.backref('occupations', lazy='joined'))
    listing={'name': name, 'description': description}

    def __init__(self, name, description, created_at, updated_at):
        self.name = name
        self.created_at = created_at
        self.description = description
        self.updated_at = updated_at
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description': self.description,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
        }