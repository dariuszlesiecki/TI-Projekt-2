from flask import Flask, current_app

import os


app = Flask(__name__)

from . import db
from app import routes
from . import auth
app.register_blueprint(auth.bp)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DATABASE'] = 'app/baza.db'


