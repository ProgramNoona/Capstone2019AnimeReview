# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
routes.py
"""

from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AnimeForm, RegisterUserForm, SearchUserForm, DeletePostForm, SearchAnimeForm
from flaskapp.models import User, Post, AnimeSeries, Genre, AnimeGenre, Studio, AnimeStudio, Media, AnimeMedia, Producer, AnimeProducer, UserRating, UserPassList
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.suggestedcontent import SuggestedContent
from flaskapp.utilities import AnimeSortQuery, save_picture, save_thumbnail, recentPost, randomAnime, getAnime, getGenre, getMedia, getProducer, getStudio, RatingCalculation

@app.route("/")
@app.route("/home")
def home():
    suggestedAnime = SuggestedContent(current_user)
    count2 = 4
    animes, animes2 = AnimeSortQuery(count2)
    randomAnimeChoice = randomAnime()
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    return render_template('home.html', animes=animes, animes2=animes2, image_file=image_file, post=post, suggestedAnime=suggestedAnime, posts=posts, randomAnimeChoice=randomAnimeChoice)

@app.route("/about")
def about():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    return render_template('about.html', title='About', suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
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
    suggestedAnime = SuggestedContent(current_user)
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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
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
    image_file2 = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, image_file2=image_file2, form=form, suggestedAnime=suggestedAnime, posts=posts)

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
    suggestedAnime = SuggestedContent(current_user)
    form = AnimeForm()
    if form.validate_on_submit():
        animeTitle = form.animeTitle.data
        anime = AnimeSeries(animeTitle=form.animeTitle.data, content=form.content.data, premiered=form.premiered.data, 
                            episodes=form.episodes.data, scored=form.scored.data, scoredBy=form.scoredBy.data, thumbnail=animeTitle, 
                            pic1=animeTitle, pic2=animeTitle, briefContent=form.content.data[0:200])
        db.session.add(anime)
        db.session.commit()
        
        item = form.genre.data
        item = item.split(",")
        for i in item:
            genreTemp = AnimeGenre(animeseries_id=anime.id, genre_id=i)
            db.session.add(genreTemp)
            db.session.commit()
        item = form.media.data
        item = item.split(",")
        for i in item:
            mediaTemp = AnimeMedia(animeseries_id=anime.id, media_id=i)
            db.session.add(mediaTemp)
            db.session.commit()
        item = form.studio.data
        item = item.split(",")
        for i in item:
            studioTemp = AnimeStudio(animeseries_id=anime.id, studio_id=i)
            db.session.add(studioTemp)
            db.session.commit()
        item = form.producer.data
        item = item.split(",")
        for i in item:
            producerTemp = AnimeProducer(animeseries_id=anime.id, producer_id=i)
            db.session.add(producerTemp)
            db.session.commit()

        if form.picture.data:
            picture_file = save_thumbnail(animeTitle, form.picture.data)
            current_user.image_file = picture_file
            anime.thumbnail = picture_file
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
    suggestedAnime = SuggestedContent(current_user)
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
    suggestedAnime = SuggestedContent(current_user)
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
    suggestedAnime = SuggestedContent(current_user)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, suggestedAnime=suggestedAnime, image_file=image_file, posts=posts)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
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
    user = User.query.get_or_404(result_id)
    user_rating = UserRating.query.filter(UserRating.user_id == result_id).all()
    user_pass = UserPassList.query.filter(UserPassList.user_id == result_id).all()
    posts = Post.query.filter(Post.user_id == result_id).all()
    if posts:
        for item in posts:
            db.session.delete(item)
    if user_rating:
        for item in user_rating:
            db.session.delete(item)
    if user_pass:
        for item in user_pass:
            db.session.delete(item)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('admintools'))

@app.route("/animepage", methods=['GET', 'POST'])
@app.route("/<animeTitle>", methods=['GET', 'POST'])
def animepage(animeTitle):
    posts = recentPost()
    suggestedAnime = SuggestedContent(current_user)
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
                elif rating < 8:
                    meh = UserPassList(user_id=current_user.id, animeseries_id=animes.id)
                    db.session.add(meh)
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

    return render_template('animepage.html', animes=animes, image_file=image_file, image_file2=image_file2, posts=posts, genreList=genreList, mediaList=mediaList, producerList=producerList, studioList=studioList, form=form, animeRating=animeRating, postValidation=postValidation, userRating=userRating, suggestedAnime=suggestedAnime, posts2=posts2)

@app.route("/genrepage", methods=['GET'])
@app.route("/genre/<genre>", methods=['GET'])
def genrepage(genre):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    tempObject = Genre.query.filter(Genre.genre == genre).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('genrepage.html', animeList=animeList, image_file=image_file, genre=genre, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/mediapage", methods=['GET'])
@app.route("/media/<media>", methods=['GET'])
def mediapage(media):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    tempObject = Media.query.filter(Media.media == media).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('mediapage.html', animeList=animeList, image_file=image_file, media=media, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/producerpage", methods=['GET'])
@app.route("/producer/<producer>", methods=['GET'])
def producerpage(producer):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    tempObject = Producer.query.filter(Producer.producer == producer).first()
    animeList = getAnime(tempObject)
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
            
    return render_template('producerpage.html', animeList=animeList, image_file=image_file, producer=producer, suggestedAnime=suggestedAnime, posts=posts)

@app.route("/studiopage", methods=['GET'])
@app.route("/studio/<studio>", methods=['GET'])
def studiopage(studio):
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    tempObject = Studio.query.filter(Studio.studio == studio).first()
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
    form = SearchUserForm()
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    
    if form.validate_on_submit():
        searchVariable = form.searchVar.data
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
    suggestedAnime = SuggestedContent(current_user)
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
    suggestedAnime = SuggestedContent(current_user)
    user = User.query.filter_by(username=searchVariable).first()
    result = Post.query.filter_by(user_id=user.id).all()
    
    if form.validate_on_submit():
        post_id = form.searchVar.data
        return redirect(url_for('delete_post', post_id=post_id))

    return render_template('user_posts.html', image_file=image_file, suggestedAnime=suggestedAnime, searchVariable=searchVariable, result=result, posts=posts, form=form)

@app.route("/search_results/<searchAnime>", methods=['GET', 'POST'])
@app.route("/search_results/<searchVariable>", methods=['GET', 'POST'])
def search_results(searchVariable):
    letter = searchVariable.replace("%", "")
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    check = len(letter)
    animes = None
    animes2 = None
    if searchVariable == "TopRated" or searchVariable == "NewAdded":
        defaultAnimeList = AnimeSeries.query.all()
        count2 = len(defaultAnimeList)
        animes, animes2 = AnimeSortQuery(count2)
        if searchVariable == "TopRated":
            searchAnime = animes
            searchTitle = "Top Rated"
        elif searchVariable == "NewAdded":
            searchAnime = animes2
            searchTitle = "Newest Added"
    elif searchVariable in ('A%','B%','C%','D%','E%','F%','G%','H%','I%','J%','K%','L%','M%',
                      'N%','O%','P%','Q%','R%','S%','T%','U%','V%','W%','X%','Y%','Z%'):
        searchTitle = "Anime starting with "
        searchAnime = AnimeSeries.query.filter(AnimeSeries.animeTitle.like(searchVariable))
    else:
        searchTitle = "Anime containing "
        searchAnime = AnimeSeries.query.filter(AnimeSeries.animeTitle.like("%" + searchVariable + "%"))
        
    return render_template('search_results.html', image_file=image_file, suggestedAnime=suggestedAnime, searchVariable=searchVariable, posts=posts, searchAnime=searchAnime, letter=letter, searchTitle=searchTitle, check=check, animes=animes, animes2=animes2)

@app.route("/search", methods=['GET', 'POST'])
def search():

    form = SearchAnimeForm()
    posts = recentPost()
    image_file = url_for('static', filename='anime_thumbnail/downloads/')
    suggestedAnime = SuggestedContent(current_user)
    if form.validate_on_submit():
        searchVariable = form.searchVar.data
        return redirect(url_for('search_results', searchVariable=searchVariable))
    
    return render_template('search.html', image_file=image_file, suggestedAnime=suggestedAnime, posts=posts, form=form)

