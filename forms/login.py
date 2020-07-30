from flask import (session)
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from validators import ValidateAuth, stripData

class LoginForm(FlaskForm):
    username=StringField(label='username', validators=[DataRequired(), ValidateAuth()])
    password=PasswordField(label='password', validators=[DataRequired()])