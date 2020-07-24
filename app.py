import os
from config import DevelopmentConfig
from os import environ
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

from models import Occupation,Employee
from controllers import occupation,employee

app.register_blueprint(occupation.bp)
app.register_blueprint(employee.bp)
# app.add_url_rule('/', endpoint='index')

@app.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()