from flask import render_template
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from connexion import FlaskApp

from config import Config

def create_app():
    app = FlaskApp(__name__)
    app.add_api("swagger.yml", base_path="/api")
    return app

connex_app = create_app()
app = connex_app.app
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db,render_as_batch=True)

from app import models


@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'Doug'}
    return render_template('home.html', title='Home', user=user)
