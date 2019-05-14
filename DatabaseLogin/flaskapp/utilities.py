# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
utilities.py
"""

import os
import secrets
import random
from PIL import Image
from flaskapp import app
from flaskapp.models import Post, AnimeSeries, Genre, Studio, Media, Producer

"""
This function's purpose is to sort the anime by scored and by the most recent added
anime using the anime's id as a reference.
"""
def AnimeSortQuery(count2):
    animes = []
    animes2 = []
    defaultDict = {}
    defaultDictNew = {}
    count = 0
    defaultAnime = AnimeSeries.query.all()
    for d in defaultAnime:
        tempAnimeID = d.id
        tempScored = d.scored
        defaultDict[tempAnimeID] = tempScored
        defaultDictNew[tempAnimeID] = tempAnimeID
    defaultDictSorted = sorted(defaultDict, key=defaultDict.get, reverse=True)
    defaultDictNewest = sorted(defaultDictNew, key=defaultDictNew.get, reverse=True)
    for i in range(1,count2):
        anime = AnimeSeries.query.filter(AnimeSeries.id == defaultDictSorted[count]).first()
        anime2 = AnimeSeries.query.filter(AnimeSeries.id == defaultDictNewest[count]).first()
        animes.append(anime)
        animes2.append(anime2)
        count += 1
    return animes, animes2

"""
Takes form.picture.data and saves the picture data to a destination folder while simultaneously
creating a random hex filename and resizing the image.
"""
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i = i.resize((125,125))
    i.save(picture_path)
    return picture_fn

"""
Takes form.picture.data and saves the picture data to a destination folder while simultaneously
creating a random hex filename and resizing the image. ( only the destination and size have changed )
"""
def save_thumbnail(animeTitle, form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = animeTitle + f_ext
    picture_path = os.path.join(app.root_path, 'static/anime_thumbnail/downloads', picture_fn)
    i = Image.open(form_picture)
    i = i.resize((200,200))
    i.save(picture_path)
    return picture_fn

"""
Queries the database for most recent posts. The -1 accounts for the index. Skims from the end.
"""
def recentPost():
    try:
        post2 = Post.query.all()
        lenCount = len(post2)
        posts = post2[lenCount - 1]
    except:
        posts = ""
    return posts

"""
Queries the database for all anime and uses the random module to select a random anime
between 0 and the number of anime currently available.
"""
def randomAnime():
    defaultAnime = AnimeSeries.query.all()
    randomAnimeIndex = random.randint(1,len(defaultAnime))
    randomAnimeChoice = AnimeSeries.query.filter_by(id=randomAnimeIndex).first()
    return randomAnimeChoice

"""
strips object information to extract the anime id within the object
""" 
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

"""
strips object information to extract the genre id within the object
""" 
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

"""
strips object information to extract the media id within the object
""" 
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

"""
strips object information to extract the producer id within the object
""" 
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

"""
strips object information to extract the studio id within the object
""" 
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

"""
This function is necessary to offset the large number of people it would require
to noticeably change the rating even by a hundredth of a point. Lacking the large
userbase of the site where the csv was derived required artificial inflaction /
deflation of scores.
""" 
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

