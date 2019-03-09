# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
models.py
"""
from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class AnimeSeries(db.Model):
    id = db.Column('animeID', db.Integer, primary_key=True)
    animeTitle = db.Column('animeTitle', db.String(100), nullable=False)
    content = db.Column('content', db.Text, nullable=False)
    premiered = db.Column('premiered', db.Text, nullable=False)
    episodes = db.Column('episodes', db.Text, nullable=False, default='n/a')
    scored = db.Column('scored', db.Text, nullable=False)
    thumbnail = db.Column('thumbnail', db.LargeBinary, nullable=False, default='thumbnail.jpg')
    pic1 = db.Column('pic1', db.LargeBinary, nullable=False, default='pic1.jpg')
    pic2 = db.Column('pic2', db.LargeBinary, nullable=False, default='pic2.jpg')

    def __repr__(self):
        return f"AnimeSeries('{self.animeTitle}', '{self.content}')"

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer = db.Column(db.String(15), nullable=False)

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studio = db.Column(db.String(15), nullable=False)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeCategory = db.Column(db.String(15), nullable=False)
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(15), nullable=False)
    
    
    
    