from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SECRET_KEY'] = 'fb12af43dfdb76374241475c69bc88ab'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
