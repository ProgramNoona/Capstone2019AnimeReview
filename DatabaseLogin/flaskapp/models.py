# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
models.py
"""
from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

"""
All Model classes represent tables within the database. Primary keys are represented
by primary_key=True. Foreign keys are represented by db.ForeignKey. Several bridging
tables exist to break up many to many relationships, E.g. AnimeSeries - AnimeGenre - Genre
"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('animeseries_id', db.Integer, db.ForeignKey('animeseries.id')))

class UserPassList(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    def __repr__(self):
        return f"{self.animeseries_id}"

class UserRating(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    rating = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.String(1), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    favorites = db.relationship('AnimeSeries', secondary=favorites, backref=db.backref('favorites', lazy='dynamic'))
    ratings = db.relationship('UserRating', backref='favorites', lazy='dynamic')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'))
    
    def __repr__(self):
        return f"User: {self.author.username}" + "\n" + f" Title: {self.title}" + "\n" + f"Review: {self.content}"

class AnimeSeries(db.Model):
    __tablename__ = 'animeseries'
    id = db.Column(db.Integer, primary_key=True)
    animeTitle = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    premiered = db.Column(db.Text, nullable=False)
    episodes = db.Column(db.Text, nullable=False, default='n/a')
    scored = db.Column(db.Text, nullable=False)
    scoredBy = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=False, default='thumbnail.jpg')
    pic1 = db.Column(db.Text, nullable=False, default='pic1.jpg')
    pic2 = db.Column(db.Text, nullable=False, default='pic2.jpg')
    briefContent = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='posts', lazy=True)
    genre = db.relationship('AnimeGenre', backref='anime_genre', lazy=True)
    media = db.relationship('AnimeMedia', backref='anime_media', lazy=True)
    studio = db.relationship('AnimeStudio', backref='anime_studio', lazy=True)
    producer = db.relationship('AnimeProducer', backref='anime_producer', lazy=True)

    def __repr__(self):
        genreID = []
        for item in self.genre:
            item = str(item)
            item = item.replace("<", "")
            item = item.replace(">", "")
            item = item.replace("AnimeGenre", "")
            item = item.replace(" ", "")
            item = item.split(",")
            item = item[1]
            genreID.append(item)
        return f"{self.id}" + "-" + f"{genreID}"

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer = db.Column(db.String(30), nullable=False)
    animeseries = db.relationship('AnimeProducer', backref='producer_anime', lazy=True)

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studio = db.Column(db.String(30), nullable=False)
    animeseries = db.relationship('AnimeStudio', backref='studio_anime', lazy=True)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(30), nullable=False)
    animeseries = db.relationship('AnimeMedia', backref='media_anime', lazy=True)
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(30), nullable=False)
    animeseries = db.relationship('AnimeGenre', backref='genre_anime', lazy=True)
    
    def __repr__(self):
        return f"Tags: {self.genre}"

class AnimeMedia(db.Model):
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)

class AnimeGenre(db.Model):
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    
class AnimeStudio(db.Model):
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'), primary_key=True)
    
class AnimeProducer(db.Model):
    animeseries_id = db.Column(db.Integer, db.ForeignKey('animeseries.id'), primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'), primary_key=True)




    
    
    