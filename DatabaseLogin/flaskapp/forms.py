# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
forms.py
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is unavailable.')
            
    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is unavailable.')

class RegisterUserForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    admin = StringField('Admin Privileges (y/n)', 
                                   validators=[DataRequired(), Length(min=1, max=1)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is unavailable.')
            
    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is unavailable.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:  
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is unavailable.')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is unavailable.')
    
class PostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Review:', validators=[DataRequired()])
    rating = SelectField('Rating:', choices=[('10','10'), ('9','9'), ('8','8'), ('7','7'), ('6','6'), ('5','5'),
                                             ('4','4'), ('3','3'), ('2','2'), ('1','1')])
    submit = SubmitField('Post')
    
class AnimeForm(FlaskForm):
    animeTitle = StringField('Anime Title', validators=[DataRequired()])
    content = StringField('Synopsis', validators=[DataRequired()])
    premiered = StringField('Premiered', validators=[DataRequired(), Length(min=2, max=30)])
    episodes = StringField('Episodes', validators=[DataRequired()])
    scored = StringField('Scored', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators=[FileAllowed(['jpg'])])
    pic1 = FileField('Thumbnail', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    pic2 = FileField('Thumbnail', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')