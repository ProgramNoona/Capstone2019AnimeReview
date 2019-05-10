# -*- coding: utf-8 -*-
"""
CSC-289 - Capstone Project - Anime Review Site
@authors: Michael Blythe, Samuel Blythe, Alex Lopez, Bethany Reagan, Juan Santiago
__init__.py
"""

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
