from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField
from wtforms.validators import DataRequired, Regexp
from models.occupation import Occupation
from validators import ValidateName, ValidateById, CheckId, stripper

class JobForm(FlaskForm):
    id=HiddenField(label='id', validators=[stripper, CheckId('Job','int', 'pk'), ValidateById(Occupation,'id','Job')])
    name=StringField(label='name', validators=[DataRequired(), stripper, CheckId('Job','str','pk'), ValidateName(Occupation,'name','Name')])
    description=StringField(label='description', validators=[DataRequired(), stripper, CheckId('Job','str','pk'), ValidateName(Occupation,'description','Description')])