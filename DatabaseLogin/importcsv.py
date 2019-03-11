# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 04:13:46 2019

@author: Mike
"""
from flaskapp import app, db
from flaskapp.models import User, Post, AnimeSeries, Producer, Studio, Type, Genre
from flask import url_for
import csv
from google_images_download import google_images_download 

def main():
    name = ""
    loadCSV(name)
def loadCSV(name):
    animeList = []
    t = ""
    test = []
    thumbnail = 'thumbnail.jpg'
    pic1 = 'pic1.jpg'
    pic2 = 'pic2.jpg'
    
    animeID,name,premiered,genre,typeCategory,episodes,producer,licensor,studio,source,scored,scoredBy,members = [],[],[],[],[],[],[],[],[],[],[],[],[]

    fileName = input('Please enter the name of the CSV file: ')
    with open(fileName) as f:
        fileName = csv.reader(f)
        next(fileName, None)
        for line in fileName:
            animeID,name,premiered,genre,typeCategory,episodes,producer,licensor,studio,source,scored,scoredBy,members,briefContent,content = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14]
            briefContent = content[0:200]
            anime = [animeID,name,premiered,genre,typeCategory,episodes,producer,licensor,studio,source,scored,scoredBy,members,briefContent,content]
            thumbnail = "{}".format(name) + ".jpg"
            pic1 = "{}".format(name) + ".jpg"
            pic2 = "{}".format(name) + ".jpg"
#            imagedownloader(name)
            animeList.append(anime)
            populateDatabase(animeID,name,premiered,genre,typeCategory,episodes,producer,licensor,studio,source,scored,scoredBy,members,thumbnail,pic1,pic2,briefContent,content)
        print()
    print('done')

def populateDatabase(animeID,name,premiered,genre,typeCategory,episodes,producer,licensor,studio,source,scored,scoredBy,members,thumbnail,pic1,pic2,briefContent,content):
    db.create_all()
    
    animeTemp = AnimeSeries(animeTitle=name, content=content, premiered=premiered, episodes=episodes, 
                         scored=scored, thumbnail=thumbnail, pic1=pic1, pic2=pic2, briefContent=briefContent)
    db.session.add(animeTemp)
    producerTemp = Producer(producer=producer)
    db.session.add(producerTemp)
    studioTemp = Studio(studio=studio)
    db.session.add(studioTemp)
    typeTemp = Type(typeCategory=typeCategory)
    db.session.add(typeTemp)
    genreTemp = Genre(genre=genre, animeseries=animeTemp)
    db.session.add(genreTemp)
    
    db.session.commit()
def imagedownloader(name):
    
    response = google_images_download.googleimagesdownload()   #class instantiation
#    arguments = '{"keywords":' + name + ',"limit":3,"exact_size":"125,125","print_urls":True}'
    arguments = {"keywords":"{}".format(name),"limit":3,"exact_size":"200,200","print_urls":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    print(paths)   #printing absolute paths of the downloaded images
    return('done')
    
def renamePicture():
    print()
        
main()
