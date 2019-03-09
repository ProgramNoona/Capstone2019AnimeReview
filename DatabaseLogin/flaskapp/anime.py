# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 03:03:43 2019

@author: Mike
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date

app = Flask(__name__)

app.config['SECRET_KEY'] = '8076854d463bae4f916366d678dbfcb7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'

db = SQLAlchemy(app)

class AnimeSeries(db.Model):
    __tablename__ = 'AnimeSeries'
    id = db.Column('animeID', db.Integer, primary_key=True)
    animeTitle = db.Column('animeTitle', db.String(100), nullable=False)
    content = db.Column('content', db.Text, nullable=False)
    def __repr__(self):
        return f"AnimeSeries('{self.animeTitle}', '{self.content}')"

