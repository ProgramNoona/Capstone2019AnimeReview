# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
__init__.py
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '8076854d463bae4f916366d678dbfcb7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskapp import routes
