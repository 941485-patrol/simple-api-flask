from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.validators import DataRequired
from models.occupation import Occupation
from validators import ValidateName, ValidateById, stripper

class JobForm(FlaskForm):
    id=HiddenField(label='id', validators=[ValidateById(Occupation,'id','Job'), stripper])
    name=StringField(label='name', validators=[DataRequired(), ValidateName(Occupation,'name','Name'), stripper])
    description=StringField(label='description', validators=[DataRequired(), ValidateName(Occupation,'description','Description'), stripper])