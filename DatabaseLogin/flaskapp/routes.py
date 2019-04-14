# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
routes.py
"""
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AnimeForm, RegisterUserForm
from flaskapp.models import User, Post, AnimeSeries, Genre, AnimeGenre, Studio, AnimeStudio, Media, AnimeMedia, Producer, AnimeProducer
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    animes = AnimeSeries.query.all()
    post = Post.query.all()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    return render_template('home.html', animes=animes, image_file=image_file, post=post)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = 'n'
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=admin)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i = i.resize((125,125))
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.user_name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/anime", methods=['GET', 'POST'])
def anime():
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    form = AnimeForm()
    if form.validate_on_submit():
        anime = AnimeSeries(animeTitle=form.animeTitle.data, content=form.content.data, premiered=form.premiered.data, 
                            episodes=form.episodes.data, scored=form.scored.data, thumbnail=form.thumbnail.data, 
                            pic1=form.pic1.data, pic2=form.pic2.data, briefContent=form.content.data[0:200])
        db.session.add(anime)
        db.session.commit()
        flash('Anime added!', 'success')
        return redirect(url_for('home'))
    return render_template('anime.html', title='Anime', form=form, legend='New Anime')

@app.route("/registeruser", methods=['GET', 'POST'])
def register_user():
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    form = RegisterUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('registeruser.html', title='Register User', form=form, legend='Register User')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    try:
        if form.validate_on_submit():
            post = Post(animeseries_id=form.animeseries_id.data, title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
    except:
        print("error")
    return render_template('create_post.html', title='New post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':   
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend='Update Post')
           
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/animepage", methods=['GET', 'POST'])
@app.route("/<animeTitle>", methods=['GET', 'POST'])
def animepage(animeTitle):
    form = PostForm()
    animes = AnimeSeries.query.filter(AnimeSeries.animeTitle == animeTitle).first()
    try:
        if form.validate_on_submit():
            post = Post(animeseries_id=animes.id, title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('animepage', animeTitle=animeTitle))
    except:
        print("error")

    posts = Post.query.filter_by(animeseries_id = animes.id).all()
    genreList = getGenre(animes)
    mediaList = getMedia(animes)
    producerList = getProducer(animes)
    studioList = getStudio(animes)
    image_file = url_for('static', filename='anime_thumbnail/downloads/' + animes.animeTitle + '.jpg')
    return render_template('animepage.html', animes=animes, image_file=image_file, posts=posts, genreList=genreList, mediaList=mediaList, producerList=producerList, studioList=studioList, form=form)

@app.route("/genrepage", methods=['GET'])
@app.route("/genre/<genre>", methods=['GET'])
def genrepage(genre):
    tempObject = Genre.query.filter(Genre.genre == genre).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('genrepage.html', animeList=animeList, image_file=image_file, genre=genre)

@app.route("/mediapage", methods=['GET'])
@app.route("/media/<media>", methods=['GET'])
def mediapage(media):
    tempObject = Media.query.filter(Media.media == media).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('mediapage.html', animeList=animeList, image_file=image_file, media=media)

@app.route("/producerpage", methods=['GET'])
@app.route("/producer/<producer>", methods=['GET'])
def producerpage(producer):
    tempObject = Producer.query.filter(Producer.producer == producer).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('producerpage.html', animeList=animeList, image_file=image_file, producer=producer)

@app.route("/studiopage", methods=['GET'])
@app.route("/studio/<studio>", methods=['GET'])
def studiopage(studio):
    tempObject = Studio.query.filter(Studio.studio == studio).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('studiopage.html', animeList=animeList, image_file=image_file, studio=studio)

def getAnime(tempObject):
    animeID = []
    animeList = []
    for item in tempObject.animeseries:
        item = str(item)
        item = item.replace("<", "")
        item = item.replace(">", "")
        item = item.replace("AnimeGenre", "")
        item = item.replace("AnimeMedia", "")
        item = item.replace("AnimeStudio", "")
        item = item.replace("AnimeProducer", "")
        item = item.replace(" ", "")
        item = item.split(",")
        item = item[0]
        animeID.append(item)
    for item in animeID:
        animeObject = AnimeSeries.query.filter_by(id=item).all()
        animeList.append(animeObject)
    return animeList

def getGenre(animes):
    genreID = []
    genreList = []
    for item in animes.genre:
        item = str(item)
        item = item.replace("<", "")
        item = item.replace(">", "")
        item = item.replace("AnimeGenre", "")
        item = item.replace(" ", "")
        item = item.split(",")
        item = item[1]
        genreID.append(item)
    for item in genreID:
        genreObject = Genre.query.filter_by(id=item).first()
        genreList.append(genreObject.genre)
    return genreList

def getMedia(animes):
    mediaID = []
    mediaList = []
    for item in animes.media:
        item = str(item)
        item = item.replace("<", "")
        item = item.replace(">", "")
        item = item.replace("AnimeMedia", "")
        item = item.replace(" ", "")
        item = item.split(",")
        item = item[1]
        mediaID.append(item)
    for item in mediaID:
        mediaObject = Media.query.filter_by(id=item).first()
        mediaList.append(mediaObject.media)
    return mediaList

def getProducer(animes):
    producerID = []
    producerList = []
    for item in animes.producer:
        item = str(item)
        item = item.replace("<", "")
        item = item.replace(">", "")
        item = item.replace("AnimeProducer", "")
        item = item.replace(" ", "")
        item = item.split(",")
        item = item[1]
        producerID.append(item)
    for item in producerID:
        producerObject = Producer.query.filter_by(id=item).first()
        producerList.append(producerObject.producer)
    return producerList

def getStudio(animes):
    studioID = []
    studioList = []
    for item in animes.studio:
        item = str(item)
        item = item.replace("<", "")
        item = item.replace(">", "")
        item = item.replace("AnimeStudio", "")
        item = item.replace(" ", "")
        item = item.split(",")
        item = item[1]
        studioID.append(item)
    for item in studioID:
        studioObject = Studio.query.filter_by(id=item).first()
        studioList.append(studioObject.studio)
    return studioList
    
    