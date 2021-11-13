from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

sql_key = os.urandom(16).hex()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = sql_key
db = SQLAlchemy(app)

from application import routes