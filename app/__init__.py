from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'Doug'}
    return render_template('home.html',title='Home',user=user)