# -*- coding: utf-8 -*-
"""
Gets you the text file that has all the content of all the medium articles you want

@author: saipr
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

#------------------------INPUTS-----------------------------------------------#

#to generalize this scraper for later use - EDIT THIS to suit your purposes
#keep all list items strings, or else this doesn't work
tags = ["gpt-3"]
years = ['2020']
months = ['06', '07']
hdr = {'User-Agent': 'Mozilla/5.0'}


#------------------------SCRAPER FUNCTIONS------------------------------------#

#INPUT - components needed to get the start link
#OUTPUT - the links of all the articles in the tag in the date range
def scrapeLinksToArticles(tag, years, months):
    startLink = "https://medium.com/tag/"+tag+"/archive/"
    articleLinks = []
    for y in years:
        yearLink = startLink + y
        for m in months:
            monLink = yearLink + "/" + m
            #open the month link and scrape all valid days (days w/ link) into drive
            req = Request(monLink,headers=hdr)
            page = urlopen(req)
            monSoup = BeautifulSoup(page)
            try: #if there are days
                allDays = list(monSoup.find("div", {"class": "col u-inlineBlock u-width265 u-verticalAlignTop u-lineHeight35 u-paddingRight0"}).find_all("div", {"class":"timebucket"}))
                for a in allDays:
                    try: #try to see if that day has a link
                        dayLink = a.find("a")['href']
                        req = Request(dayLink,headers=hdr)
                        page = urlopen(req)
                        daySoup = BeautifulSoup(page)
                        links = list(daySoup.find_all("div", {"class": "postArticle-readMore"}))
                        for l in links:
                            articleLinks.append(l.find("a")['href'])
                    except: pass
            except: #take the month's articles
                links = list(monSoup.find_all("div", {"class": "postArticle-readMore"}))
                for l in links:
                    articleLinks.append(l.find("a")['href'])
                print("issueHere")
    print("Article Links: ", len(articleLinks))
    return articleLinks

#INPUT - link to a medium article
#OUTPUT - string with all the article text
def scrapeArticle(link):
    bodyText = ""
    req = Request(link,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)    
    textBoxes = list(soup.find("article", {"class": "meteredContent"}).find_all("p"))
    for t in textBoxes:
        bodyText = bodyText + t.get_text()
    return bodyText

#------------------------PROCESS----------------------------------------------#

articleLinks = []
for tag in tags: 
    articleLinks.extend(scrapeLinksToArticles(tag, years, months))
articleLinks = set(articleLinks) #get rid of any duplicates

outPutText = open("mediumScrape.txt", "a+", encoding='utf8')
count = 0
for art in articleLinks:
    print(count)
    outPutText.write(str(scrapeArticle(art)))
    count += 1    
outPutText.close()