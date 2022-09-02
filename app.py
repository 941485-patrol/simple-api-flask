import os, datetime
from config import DevelopmentConfig
from os import environ
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(environ.get('APP_SETTINGS'))
db = SQLAlchemy(app)

from controllers import occupation,employee,user

app.register_blueprint(occupation.bp)
app.register_blueprint(employee.bp)
app.register_blueprint(user.bp)
app.json.sort_keys=True

migrate = Migrate()
migrate.init_app(app, db)
# app.add_url_rule('/', endpoint='index')

@app.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()