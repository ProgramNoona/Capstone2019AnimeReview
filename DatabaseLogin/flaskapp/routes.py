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
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AnimeForm, RegisterUserForm, SearchForm, DeletePostForm
from flaskapp.models import User, Post, AnimeSeries, Genre, AnimeGenre, Studio, AnimeStudio, Media, AnimeMedia, Producer, AnimeProducer, UserRating
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_

@app.route("/")
@app.route("/home")
def home():
    animes = AnimeSeries.query.all()
#    animes = AnimeSeries.query.limit(5)
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    return render_template('home.html', animes=animes, image_file=image_file, post=post, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/about")
def about():
    post = Post.query.all()
    lenCount = len(post)
    posts = post[lenCount - 1]
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    return render_template('about.html', title='About', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
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
    return render_template('register.html', title='Register', form=form, suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
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
    return render_template('login.html', title='Login', form=form, suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

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
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
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
    return render_template('account.html', title='Account', image_file=image_file, form=form, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/anime", methods=['GET', 'POST'])
@login_required
def anime():
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    form = AnimeForm()
    if form.validate_on_submit():
        anime = AnimeSeries(animeTitle=form.animeTitle.data, content=form.content.data, premiered=form.premiered.data, 
                            episodes=form.episodes.data, scored=form.scored.data, thumbnail=form.thumbnail.data, 
                            pic1=form.pic1.data, pic2=form.pic2.data, briefContent=form.content.data[0:200])
        db.session.add(anime)
        db.session.commit()
        flash('Anime added!', 'success')
        return redirect(url_for('home'))
    return render_template('anime.html', title='Anime', form=form, legend='New Anime', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/registeruser", methods=['GET', 'POST'])
@login_required
def register_user():
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    form = RegisterUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('registeruser.html', title='Register User', form=form, legend='Register User', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
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
    return render_template('create_post.html', title='New post', form=form, legend='New Post', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
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
    return render_template('create_post.html', title='Update post', form=form, legend='Update Post', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    suggestedAnime = SuggestedContent()
    post = Post.query.get_or_404(post_id)
    ratingObject = UserRating.query.filter(UserRating.animeseries_id == post.animeseries_id).first()
    db.session.delete(post)
    db.session.delete(ratingObject)
    db.session.commit()
    flash('Post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<result_id>/delete", methods=['POST'])
@login_required
def delete_user(result_id):
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    suggestedAnime = SuggestedContent()
    user = User.query.get_or_404(result_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('admintools'))

@app.route("/animepage", methods=['GET', 'POST'])
@app.route("/<animeTitle>", methods=['GET', 'POST'])
def animepage(animeTitle):
    posts = recentPost()
    suggestedAnime = SuggestedContent()
    form = PostForm()
    postValidation = ""
    animes = AnimeSeries.query.filter(AnimeSeries.animeTitle == animeTitle).first()
    userRating = UserRating.query.filter(UserRating.animeseries_id == animes.id).all()
    
    animeRating = animes.scored
    
    try:
        if form.validate_on_submit():
            post = Post(animeseries_id=animes.id, title=form.title.data, content=form.content.data, author=current_user)
            fav = UserRating(user_id=current_user.id, animeseries_id=animes.id, rating=form.rating.data)
            try:
                rating=int(form.rating.data)
                if rating >= 8:
                    animes.favorites.append(current_user)
                scored, scoredBy, rating = float(animes.scored), float(animes.scoredBy), float(rating)
                scored, scoredBy = RatingCalculation(rating, scored, scoredBy)
                scored, scoredBy = str(round(scored, 2)), str(scoredBy)
                animes.scored, animes.scoredBy = scored, scoredBy
            except:
                print("error2")
            db.session.add(post)
            db.session.add(fav)
            db.session.commit()
            flash('Your post has been created!', 'success')
            flash( scored, 'success')
            return redirect(url_for('animepage', animeTitle=animeTitle))
    except:
        print("error")

    posts2 = Post.query.filter_by(animeseries_id = animes.id).all()
    try:
        for post in posts2:
            if post.user_id == current_user.id:
                postValidation = "exists"
    except:
        print("No user ID found")
    genreList = getGenre(animes)
    mediaList = getMedia(animes)
    producerList = getProducer(animes)
    studioList = getStudio(animes)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    image_file2 = url_for('static', filename='gallery_thumbnail/')
#    image_file = url_for('static', filename='anime_thumbnail/downloads/' + animes.animeTitle + '.jpg')
    return render_template('animepage.html', animes=animes, image_file=image_file, image_file2=image_file2, posts=posts, genreList=genreList, mediaList=mediaList, producerList=producerList, studioList=studioList, form=form, animeRating=animeRating, postValidation=postValidation, userRating=userRating, suggestedAnime=suggestedAnime, posts2=posts2)

@app.route("/genrepage", methods=['GET'])
@app.route("/genre/<genre>", methods=['GET'])
def genrepage(genre):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    tempObject = Genre.query.filter(Genre.genre == genre).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('genrepage.html', animeList=animeList, image_file=image_file, genre=genre, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/mediapage", methods=['GET'])
@app.route("/media/<media>", methods=['GET'])
def mediapage(media):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    tempObject = Media.query.filter(Media.media == media).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('mediapage.html', animeList=animeList, image_file=image_file, media=media, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/producerpage", methods=['GET'])
@app.route("/producer/<producer>", methods=['GET'])
def producerpage(producer):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    tempObject = Producer.query.filter(Producer.producer == producer).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('producerpage.html', animeList=animeList, image_file=image_file, producer=producer, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/studiopage", methods=['GET'])
@app.route("/studio/<studio>", methods=['GET'])
def studiopage(studio):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    tempObject = Studio.query.filter(Studio.studio == studio).first()
#    animeGenreObject = AnimeGenre.query.filter(AnimeGenre.genre_id == genreObject.id).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('studiopage.html', animeList=animeList, image_file=image_file, studio=studio, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/admintools", methods=['GET', 'POST'])
@login_required
def admintools():
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    result = ""
    searchVariable = ""
    form = SearchForm()
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    
    if form.validate_on_submit():
        searchVariable = form.searchVar.data
#        result = User.query.filter_by(username=form.searchVar.data).first()
#        result = User.query.filter(User.username.like(form.searchVar.data))
        return redirect(url_for('results', searchVariable=searchVariable))
        
    return render_template('admintools.html', image_file=image_file, form=form, suggestedAnime=suggestedAnime, result=result, searchVariable=searchVariable, posts=posts)

@app.route("/results/<searchVariable>", methods=['GET', 'POST'])
@login_required
def results(searchVariable):
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    result = User.query.filter_by(username=searchVariable).first()
    return render_template('results.html', image_file=image_file, suggestedAnime=suggestedAnime, searchVariable=searchVariable, result=result, posts=posts)

@app.route("/user_posts/<searchVariable>", methods=['GET', 'POST'])
@login_required
def user_posts(searchVariable):
    try:
        if current_user.admin != 'y':
            abort(403)
    except:
        abort(403)
    form = DeletePostForm()
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent()
    user = User.query.filter_by(username=searchVariable).first()
    result = Post.query.filter_by(user_id=user.id).all()
    
    if form.validate_on_submit():
        post_id = form.searchVar.data
        return redirect(url_for('delete_post', post_id=post_id))

    return render_template('user_posts.html', image_file=image_file, suggestedAnime=suggestedAnime, searchVariable=searchVariable, result=result, posts=posts, form=form)

def recentPost():
    post2 = Post.query.all()
    lenCount = len(post2)
    posts = post2[lenCount - 1]
    return posts

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
    
def RatingCalculation(rating, scored, scoredBy):
    scoredBy = scoredBy + 1
    total = scored * scoredBy
    if rating == 10:
        total += (rating + 5000)
    elif rating == 9:
        total += (rating + 4000)
    elif rating == 8:
        total += (rating + 3000)
    elif rating == 7:
        total += (rating + 2000)
    elif rating == 6:
        total += (rating + 1000)
    elif rating == 5:
        total += (rating)
    elif rating == 4:
        total += (rating - 1000)
    elif rating == 3:
        total += (rating - 2000)
    elif rating == 2:
        total += (rating - 3000)
    elif rating == 1:
        total += (rating - 4000)
    scored = (total / scoredBy)
    scoredBy = int(scoredBy)
    return scored, scoredBy


def SuggestedContent():
    testList = []
    favList = []
    mergeList = []
    numberCount = []
    genreList = []
    topGenreCount = []
    suggestedAnimeList = []
    suggestedAnimeCount = []
    defaultDictSorted = []
    temp = []
    usedAnimeList = []
    suggestedAnimeSet = set()
    defaultDict = {}
    genreDict = {}
    suggestedAnimeDict = {}
    count = 1
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    
    try:
        fav = current_user.favorites
        for item in fav:
            item = str(item)
            item = item.replace("[", "")
            item = item.replace("]", "")
            item = item.replace("'", "")
            item = item.replace(" ", "")
            item2 = item.split("-")
            item = item2[1]
            favItem = item2[0]
            item = item.split(",")
            testList.append(item)
            favList.append(favItem)
        
    
        for item in testList:
            temp += item
        for item in temp:
            mergeList.append(int(item))
        mergeSet = set(mergeList)
        mergeList2 = list(mergeSet)
        mergeList2.sort()
        for item in mergeList2:
            number = mergeList.count(item)
            numberCount.append(number)
            genreList.append(mergeList2[count1])
            count += 1
            count1 += 1
    
        for item in mergeList2:
            value = numberCount[count2]
            key = genreList[count2]
            genreDict[key] = value
            count2 += 1
        
        genreDictSorted = sorted(genreDict, key=genreDict.get, reverse=True)
        
        for item in genreDictSorted:
            topGenreCount.append(genreDictSorted[count3])
            count3 += 1
        
        test3 = AnimeGenre.query.filter(AnimeGenre.genre_id.in_(topGenreCount)).all()
        
        for item in test3:
            item = str(item)
            item = item.replace("<", "")
            item = item.replace(">", "")
            item = item.replace("AnimeGenre", "")
            item = item.replace(" ", "")
            item = item.split(",")
            item = item[0]
            suggestedAnimeList.append(item)
            
        for i in range(1,len(suggestedAnimeList) + 1):
            suggestedAnimeSet.add(suggestedAnimeList[count4])
            count4 += 1
        usedAnimeList = list(suggestedAnimeSet)
        usedAnimeList.sort()
        
        for item in usedAnimeList:
            number2 = suggestedAnimeList.count(item)
            suggestedAnimeCount.append(number2)
        
        for i in range(1,len(usedAnimeList) + 1):
            value = suggestedAnimeCount[count5]
            key = usedAnimeList[count5]
            suggestedAnimeDict[key] = value
            count5 += 1
        suggestedAnimeDictSorted = sorted(suggestedAnimeDict, key=suggestedAnimeDict.get, reverse=True)
        for item in suggestedAnimeDictSorted:
            tempSuggestedAnime = suggestedAnimeDictSorted[count6]
            if tempSuggestedAnime in (favList):
                count6 += 1
            else:
                break
        suggestedAnime = AnimeSeries.query.filter(AnimeSeries.id == tempSuggestedAnime).first()
        
    except:
        defaultAnime = AnimeSeries.query.all()
        for d in defaultAnime:
            tempAnimeID = d.id
            tempScored = d.scored
            defaultDict[tempAnimeID] = tempScored
        defaultDictSorted = sorted(defaultDict, key=defaultDict.get, reverse=True)
        suggestedAnime = AnimeSeries.query.filter(AnimeSeries.id == defaultDictSorted[0]).first()
    
    return suggestedAnime

@app.route("/test", methods=['GET', 'POST'])
def SuggestedContentTest():
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    posts = recentPost()

    
    testList = []
    favList = []
    mergeList = []
    numberCount = []
    genreList = []
    topGenreCount = []
    suggestedAnimeList = []
    suggestedAnimeCount = []
    defaultDictSorted = []
    temp = []
    usedAnimeList = []
    suggestedAnimeSet = set()
    defaultDict = {}
    genreDict = {}
    suggestedAnimeDict = {}
    count = 1
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    
    try:
        fav = current_user.favorites
        for item in fav:
            item = str(item)
            item = item.replace("[", "")
            item = item.replace("]", "")
            item = item.replace("'", "")
            item = item.replace(" ", "")
            item2 = item.split("-")
            item = item2[1]
            favItem = item2[0]
            item = item.split(",")
            testList.append(item)
            favList.append(favItem)
        
    
        for item in testList:
            temp += item
        for item in temp:
            mergeList.append(int(item))
        mergeSet = set(mergeList)
        mergeList2 = list(mergeSet)
        mergeList2.sort()
        for item in mergeList2:
            number = mergeList.count(item)
            numberCount.append(number)
            genreList.append(mergeList2[count1])
            count += 1
            count1 += 1
    
        for item in mergeList2:
            value = numberCount[count2]
            key = genreList[count2]
            genreDict[key] = value
            count2 += 1
        
        genreDictSorted = sorted(genreDict, key=genreDict.get, reverse=True)
        
        for item in genreDictSorted:
            topGenreCount.append(genreDictSorted[count3])
            count3 += 1
        
        test3 = AnimeGenre.query.filter(AnimeGenre.genre_id.in_(topGenreCount)).all()
        
        for item in test3:
            item = str(item)
            item = item.replace("<", "")
            item = item.replace(">", "")
            item = item.replace("AnimeGenre", "")
            item = item.replace(" ", "")
            item = item.split(",")
            item = item[0]
            suggestedAnimeList.append(item)
            
        for i in range(1,len(suggestedAnimeList) + 1):
            suggestedAnimeSet.add(suggestedAnimeList[count4])
            count4 += 1
        usedAnimeList = list(suggestedAnimeSet)
        usedAnimeList.sort()
        
        for item in usedAnimeList:
            number2 = suggestedAnimeList.count(item)
            suggestedAnimeCount.append(number2)
        
        for i in range(1,len(usedAnimeList) + 1):
            value = suggestedAnimeCount[count5]
            key = usedAnimeList[count5]
            suggestedAnimeDict[key] = value
            count5 += 1
        suggestedAnimeDictSorted = sorted(suggestedAnimeDict, key=suggestedAnimeDict.get, reverse=True)
        for item in suggestedAnimeDictSorted:
            tempSuggestedAnime = suggestedAnimeDictSorted[count6]
            if tempSuggestedAnime in (favList):
                count6 += 1
            else:
                break
        suggestedAnime = AnimeSeries.query.filter(AnimeSeries.id == tempSuggestedAnime).first()
        
    except:
        defaultAnime = AnimeSeries.query.all()
        for d in defaultAnime:
            tempAnimeID = d.id
            tempScored = d.scored
            defaultDict[tempAnimeID] = tempScored
        defaultDictSorted = sorted(defaultDict, key=defaultDict.get, reverse=True)
        suggestedAnime = AnimeSeries.query.filter(AnimeSeries.id == defaultDictSorted[0]).first()
    
    return render_template('test.html', testList=testList, mergeList=mergeList, numberCount=numberCount, genreList=genreList, count=count, genreDict=genreDict, genreDictSorted=genreDictSorted, test3=test3, suggestedAnimeList=suggestedAnimeList, usedAnimeList=usedAnimeList, suggestedAnimeCount=suggestedAnimeCount, suggestedAnimeDict=suggestedAnimeDict, mergeSet=mergeSet, suggestedAnimeDictSorted=suggestedAnimeDictSorted, suggestedAnime=suggestedAnime, mergeList2=mergeList2, fav=fav, favList=favList, defaultDict=defaultDict, defaultDictSorted=defaultDictSorted, image_file=image_file, posts=posts)