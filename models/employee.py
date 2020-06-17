from app import db
class Employee(db.Model):
    __tablename__ = 'employees'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    created_at=db.Column(db.DateTime(timezone=True))
    updated_at=db.Column(db.DateTime(timezone=True))
    occupations_id=db.Column(db.Integer, db.ForeignKey('occupations.id'))
    listing={'name':name, 'email':email, 'occupations_id':occupations_id}

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
