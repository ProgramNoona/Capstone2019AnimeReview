# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 04:13:46 2019

@author: Mike
"""
from flaskapp import app, db, bcrypt
from flaskapp.models import User, Post, AnimeSeries, Producer, Studio, Media, Genre, AnimeGenre, AnimeMedia, AnimeProducer, AnimeStudio
from flask import url_for
import csv
from google_images_download import google_images_download 

def main():
    CreateAdmin()
    PopulateDatabase()
    
def CreateAdmin():
    username="admin"
    email="admin@anirater.com"
    password="apple"
    admin="y"
    db.create_all()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, admin=admin)
    db.session.add(user)
    db.session.commit()
    
def PopulateDatabase():
    count = 0
    genreSet = set()
    mediaSet = set()
    producerSet = set()
    studioSet = set()
    thumbnail = 'thumbnail.jpg'
    pic1 = 'pic1.jpg'
    pic2 = 'pic2.jpg'
    
    fileName = input('Please enter the name of the CSV file: ')
    with open(fileName) as f:
        fileName = csv.reader(f)
        next(fileName, None)
        for line in fileName:
            animeID,name,premiered,genre,media,episodes,producer,licensor,studio,source,scored,scoredBy,members,briefContent,content = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]
            briefContent = content[0:200]
            thumbnail = "{}".format(name) + ".jpg"
            pic1 = "{}".format(name) + ".jpg"
            pic2 = "{}".format(name) + ".jpg"
            genre,producer,studio = genre.replace("[", ""), producer.replace("[", ""), studio.replace("[", "")
            genre,producer,studio = genre.replace("]", ""), producer.replace("]", ""), studio.replace("]", "")
            genre,producer,studio = genre.replace("'", ""), producer.replace("'", ""), studio.replace("'", "")
            genre,producer,studio = genre.replace(" ", ""), producer.replace(" ", ""), studio.replace(" ", "")
            genreList,producerList,studioList = genre.split(","), producer.split(","), studio.split(",")
            count += 1
            animeTemp = AnimeSeries(animeTitle=name, content=content, premiered=premiered, episodes=episodes, 
                                    scored=scored, scoredBy=scoredBy, thumbnail=thumbnail, pic1=pic1, pic2=pic2, briefContent=briefContent)
            db.session.add(animeTemp)
            mediaSet.add(media)
            for item in genreList:
                genreSet.add(item)
            for item in producerList:
                producerSet.add(item)
            for item in studioList:
                studioSet.add(item)
        genreList = list(genreSet)
        mediaList = list(mediaSet)
        producerList = list(producerSet)
        studioList = list(studioSet)
        genreList.sort(),mediaList.sort(),producerList.sort(),studioList.sort()
        

    print('done')
    
    for genre in genreList:
        genreTemp = Genre(genre=genre)
        db.session.add(genreTemp)
    for media in mediaList:
        mediaTemp = Media(media=media)
        db.session.add(mediaTemp)
    for producer in producerList:
        producerTemp = Producer(producer=producer)
        db.session.add(producerTemp)
    for studio in studioList:
        studioTemp = Studio(studio=studio)
        db.session.add(studioTemp)
    db.session.commit()
    
    loadCSV()
    db.session.commit()
    
def populateGenreTable():
    pass

def loadCSV():
    count = 0
    fileName = "anime.csv"
    with open(fileName) as f:
        fileName = csv.reader(f)
        next(fileName, None)
        for line in fileName:
            genre,media,producer,studio = line[3],line[4],line[6],line[8]
            genre,producer,studio = genre.replace("[", ""), producer.replace("[", ""), studio.replace("[", "")
            genre,producer,studio = genre.replace("]", ""), producer.replace("]", ""), studio.replace("]", "")
            genre,producer,studio = genre.replace("'", ""), producer.replace("'", ""), studio.replace("'", "")
            genre,producer,studio = genre.replace(" ", ""), producer.replace(" ", ""), studio.replace(" ", "")
            genreList,producerList,studioList = genre.split(","), producer.split(","), studio.split(",")
            count += 1
            for item in genreList:
                GenreQuery(item, count)
            for item in producerList:
                ProducerQuery(item, count)
            for item in studioList:
                StudioQuery(item, count)
            item = media
            MediaQuery(item, count)

def GenreQuery(item, count):
    item = str(item)
    print(item)
    genreObject = Genre.query.filter_by(genre=item).first()
    genre_id = genreObject.id
    genreTemp = AnimeGenre(animeseries_id=count, genre_id=genre_id)
    db.session.add(genreTemp)
    
def MediaQuery(item, count):
    item = str(item)
    print(item)
    mediaObject = Media.query.filter_by(media=item).first()
    media_id = mediaObject.id
    mediaTemp = AnimeMedia(animeseries_id=count, media_id=media_id)
    db.session.add(mediaTemp)
    
def ProducerQuery(item, count):
    item = str(item)
    print(item)
    producerObject = Producer.query.filter_by(producer=item).first()
    producer_id = producerObject.id
    producerTemp = AnimeProducer(animeseries_id=count, producer_id=producer_id)
    db.session.add(producerTemp)
    
def StudioQuery(item, count):
    item = str(item)
    print(item)
    studioObject = Studio.query.filter_by(studio=item).first()
    studio_id = studioObject.id
    studioTemp = AnimeStudio(animeseries_id=count, studio_id=studio_id)
    db.session.add(studioTemp)

def imagedownloader(name):
    
    response = google_images_download.googleimagesdownload()   #class instantiation
#    arguments = '{"keywords":' + name + ',"limit":3,"exact_size":"125,125","print_urls":True}'
    arguments = {"keywords":"{}".format(name),"limit":3,"exact_size":"200,200","print_urls":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images
    return('done')
    
def renamePicture():
    """
    for item in test.genre:
    item = str(item)
    item = item.replace("<", "")
    item = item.replace(">", "")
    item = item.replace("AnimeGenre", "")
    item = item.replace(" ", "")
    print(item)
    itemList = item.split(",")
    print("animeid "  + itemList[0] + ", genreid " + itemList[1])
    """
    print()
        
main()
