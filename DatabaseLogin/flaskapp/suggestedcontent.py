# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
suggestedcontent.py
"""

import random
from flaskapp.models import AnimeSeries, AnimeGenre, UserPassList

"""
This function takes the favorites of the current user, examines the genre tags 
of each anime in the favorites list, and tallies the genres. After the iteration 
process, the tallied genre tags are sorted from the highest count to the lowest. 
The highest tallied genre is then added to a list where a query is performed to 
search for any anime containing one or all of the genres on the list. The anime 
returned are then sorted once more from the highest number of related genre tags 
to lowest. The highest matching anime (first on the list, index 0) will then be 
chosen as the suggested anime UNLESS that anime is found within the users favorites 
list (anime that received a rating of 8 or higher are automatically added to the 
users favorite list) or found within the user's pass list (anime that got a 7 or 
lower rating by the user). If this is the case, 1 is added to the index to move 
it down the line to “the next best” relevant anime and is then checked against the 
favorite list and pass list again. If the user is not logged in or has not left a 
review, a random anime is chosen from a selection of 10 of the top rated anime.
"""
def SuggestedContent(current_user):
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
    passList = []
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
        try:
            passObject = UserPassList.query.filter_by(user_id=current_user.id).all()
            for k in passObject:
                k = k.animeseries_id
                passList.append(k)
        except:
            pass
        
        for item in fav:
            item = str(item)
            item = item.replace("[", "")
            item = item.replace("]", "")
            item = item.replace("'", "")
            item = item.replace(" ", "")
            item2 = item.split("-")
            item = item2[1]
            favItem = int(item2[0])
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
            tempSuggestedAnime = int(suggestedAnimeDictSorted[count6])
            if tempSuggestedAnime in favList or tempSuggestedAnime in passList:
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
        randomIndex = [1,2,3,4,5,6,7,8,9,10]
        randomIndexChoice = random.choice(randomIndex)
        suggestedAnime = AnimeSeries.query.filter(AnimeSeries.id == defaultDictSorted[randomIndexChoice]).first()
    
    return suggestedAnime
