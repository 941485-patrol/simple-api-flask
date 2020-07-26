from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp, InputRequired, Length
from models.occupation import Occupation
from validators import ValidateName, ValidateById, IsIdNumber, IsIdPathValid, stripData

class JobForm(FlaskForm):
    id=HiddenField(
        label='id', 
        validators=[
            stripData, 
            IsIdNumber(idData='field-data'), 
            IsIdPathValid(), 
            ValidateById(Occupation,'Job',pk=True)
            ])
    name=StringField(
        label='name', 
        validators=[
            DataRequired(),
            stripData, 
            Length(min=2, max=50, message='Minimum 2 and maximum 50 characters.'),
            IsIdNumber(idData='form-data'), 
            IsIdPathValid(), 
            ValidateName(Occupation,'name','Name')
            ])
    description=StringField(
        label='description', 
        validators=[
            DataRequired(), 
            stripData,
            Length(min=5, max=100, message='Minimum 5 and maximum 100 characters.'),
            IsIdNumber(idData='form-data'), 
            IsIdPathValid(), 
            ValidateName(Occupation,'description','Description')
            ])