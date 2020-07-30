from app import db
from flask import jsonify
class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(255))
    created_at=db.Column(db.DateTime(timezone=True))
    updated_at=db.Column(db.DateTime(timezone=True))
    listing={'username': username}

    def __init__(self, username, password, created_at, updated_at):
        self.username = username
        self.created_at = created_at
        self.password = password
        self.updated_at = updated_at
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'username': self.username,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
        }