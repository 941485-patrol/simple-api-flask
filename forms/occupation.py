from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp, InputRequired
from models.occupation import Occupation
from validators import ValidateName, ValidateById, IsIdNumber, IsIdPathValid, stripData

class JobForm(FlaskForm):
    id=HiddenField(label='id', validators=[stripData, IsIdNumber(idData='field-data'), IsIdPathValid(), ValidateById(Occupation,'Job',pk=True)])
    name=StringField(label='name', validators=[DataRequired(), stripData, IsIdNumber(idData='form-data'), IsIdPathValid(), ValidateName(Occupation,'name','Name')])
    description=StringField(label='description', validators=[DataRequired(), stripData, IsIdNumber(idData='form-data'), IsIdPathValid(), ValidateName(Occupation,'description','Description')])