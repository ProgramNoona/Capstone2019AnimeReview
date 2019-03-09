# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 05:08:50 2019

@author: Mike
"""

from datetime import datetime
from flaskapp import app, db, bcrypt
from flaskapp.models import User, Post, AnimeSeries

def main():
    print('CRUD: Database modifications menu')
    print()
    print('1. Query users')
    print('2. Query posts')
    print('3. Query anime')
    print('4. Exit')
    print()
    userChoice = input('Choose an option: ')
    
    if userChoice in ('1'):
        usersQuery()
    elif userChoice in ('2'):
        postsQuery()
    elif userChoice in ('3'):
        animeQuery()
    elif userChoice in ('4'):
        exit()
    else:
        print()
        print('Please choose an option above')
        print()
        main()
        
def usersQuery():
    print('CRUD: Users table modifications')
    print()
    print('1. View users')
    print('2. Add users')
    print('3. Delete users')
    print('4. main menu')
    print()
    userChoice = input('Choose an option: ')
    
    if userChoice in ('1'):
        users = User.query.all()
        for u in users:
            print(u)
        print()
        usersQuery()
    elif userChoice in ('2'):
        try:
            username1 = input('Username: ')
            email1 = input('Email: ')
            password1 = input('Password: ')
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            user1 = User(username=username1, email=email1, image_file='default.jpg', password=hashed_password)
            userChoice2 = input('Are you sure you want to commit the change? (y/n)')
            if userChoice2 in ('y', 'Y'):
                db.session.add(user1)
                db.session.commit()
                print('User added!')
                print()
                usersQuery()
            else:
                usersQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('3'):
        try:
            user1 = input('Username to delete: ')
            user1 = User.query.filter(User.username == user1).one()
            if user1 == []:
                print('User not found')
                usersQuery()
                print()
            else:
                print('Found user!')
                print(user1)
                print()
                userChoice2 = input('Are you sure you want to commit the change? (y/n)')
                if userChoice2 in ('y', 'Y'):
                    db.session.delete(user1)
                    db.session.commit()
                    print()
                    print('User deleted!')
                    print()
                    usersQuery()
                else:
                    usersQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('4'):
        main()
    else:
        print()
        print('Please choose an option above')
        print()
        usersQuery()
        
def postsQuery():
    print('CRUD: Posts table modifications')
    print()
    print('1. View posts')
    print('2. Add posts')
    print('3. Delete posts')
    print('4. main menu')
    print()
    userChoice = input('Choose an option: ')
    
    if userChoice in ('1'):
        posts = Post.query.all()
        for p in posts:
            print(p)
        print()
        postsQuery()
    elif userChoice in ('2'):
        try:
            title1 = input('Title: ')
            content1 = input('Content: ')
            user_id = input('User id: ')
            post1 = Post(title=title1, date_posted=datetime.utcnow(), content=content1, user_id=user_id)
            userChoice2 = input('Are you sure you want to commit the change? (y/n)')
            if userChoice2 in ('y', 'Y'):
                db.session.add(post1)
                db.session.commit()
                print('Post added!')
                print()
                postsQuery()
            else:
                postsQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('3'):
        try:
            post1 = input('Post_ID to delete: ')
            post1 = Post.query.filter(Post.id == post1).one()
            if post1 == []:
                print('Post not found')
                postsQuery()
                print()
            else:
                print('Found post!')
                print(post1)
                print()
                userChoice2 = input('Are you sure you want to commit the change? (y/n)')
                if userChoice2 in ('y', 'Y'):
                    db.session.delete(post1)
                    db.session.commit()
                    print('Post Deleted!')
                    print()
                    postsQuery()
                else:
                    postsQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('4'):
        main()
    else:
        print()
        print('Please choose an option above')
        print()
        postsQuery()
        
def animeQuery():
    print('CRUD: Anime table modifications')
    print()
    print('1. View anime')
    print('2. Add anime')
    print('3. Delete anime')
    print('4. main menu')
    print()
    userChoice = input('Choose an option: ')
    
    if userChoice in ('1'):
        anime = AnimeSeries.query.all()
        for a in anime:
            print(a)
        print()
        animeQuery()
    elif userChoice in ('2'):
        try:
            animeTitle = input('Anime title: ')
            content = input('Synopsis: ')
            anime1 = AnimeSeries(animeTitle=animeTitle, content=content)
            userChoice2 = input('Are you sure you want to commit the change? (y/n)')
            if userChoice2 in ('y', 'Y'):
                db.session.add(anime1)
                db.session.commit()
                print('Anime added!')
                print()
                animeQuery()
            else:
                animeQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('3'):
        try:
            title1 = input('Anime title to delete: ')
            anime1 = AnimeSeries.query.filter(AnimeSeries.animeTitle == title1).first()
            if anime1 == []:
                print('Anime not found')
                animeQuery()
                print()
            else:
                print('Found anime!')
                print(anime1)
                print()
                userChoice2 = input('Are you sure you want to commit the change? (y/n)')
                if userChoice2 in ('y', 'Y'):
                    db.session.delete(anime1)
                    db.session.commit()
                    print()
                    print('Anime deleted!')
                    print()
                    animeQuery()
                else:
                    animeQuery()
        except:
            print('An error has occured. Check input.')
            print()
            db.session.rollback()
            main()
            
    elif userChoice in ('4'):
        main()
    else:
        print()
        print('Please choose an option above')
        print()
        animeQuery()
main()