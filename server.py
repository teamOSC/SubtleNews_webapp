#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
from flask import request
import os
import json
import feedparser
from datetime import datetime,timedelta
from dateutil import parser as string2date
from collections import Counter
import urllib
import logging
import random
app = flask.Flask(__name__)

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return unicode("अभी अभी", "UTF-8")
        if second_diff < 120:
            return unicode("1 मिनट पहले", "UTF-8")
        if second_diff < 3600:
            return str(second_diff / 60) + unicode(" मिनट पहले", "UTF-8")
        if second_diff < 7200:
            return unicode("1 घंटा पहले", "UTF-8")
        if second_diff < 86400:
            return str(second_diff / 3600) + unicode(" घंटे पहले", "UTF-8")
    if day_diff == 1:
        return unicode("1 दिन पहले", "UTF-8")
    if day_diff < 7:
        return str(day_diff) + unicode(" दिन पहले", "UTF-8")
    if day_diff < 31:
        return str(day_diff / 7) + unicode(" सप्ताह पहले", "UTF-8")
    if day_diff < 365:
        return str(day_diff / 30) + unicode(" माह पहले", "UTF-8")
    return str(day_diff / 365) + unicode(" वर्ष पहले", "UTF-8")

def get_image(desc):
    temp = desc.split('src="')[-1]
    img = temp.split('"')[0]
    if not img.startswith("https://t"):
        img = "http://i.imgur.com/KU1vsAS.png"
    print img
    return img

def scrape_news():
    categories = "all,w,n,b,e,s,h".split(',')
    news_dict = {}
    for category in categories:
        print category
        #available categories ,w,n,b,e,s
        if category == "all":
            url1 = 'https://news.google.com/news/feeds?cf=all&hl=hi&output=rss&ned=hi_in'
            url2 = 'https://news.google.com/news/feeds?cf=all&hl=hi&output=rss&ned=hi_in&topic=h'
            rss = dict(feedparser.parse(url1).items() +feedparser.parse(url2).items())
        else:
            url = 'https://news.google.com/news/feeds?cf=all&hl=hi&output=rss&ned=hi_in&topic=%s'%(category)
            rss = feedparser.parse(url)
        category_news = []
        for item in rss['entries']:
            link = item['link']
            d= {}
            #removing the google stuff from the url
            d['link'] = "https://www.instapaper.com/text?u=" + link[link.rfind('&url=')+5:]
            d['title'] = item['title']
            d['description'] = item['description']
            d['image'] = get_image(item['description'])
            n = d['title'].rfind('-')
            d['source'] = d['title'][n+1: ]
            if d['source'] == '7':
                d['source'] = "NDTV 24-7"
            d['title'] = d['title'][:n]
            date_object = string2date.parse(item['published'])
            date_object = date_object.replace(tzinfo=None)
            #date_object = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S GMT')
            d['date']= pretty_date(date_object+timedelta( 0, 5*60*60 + 30*60 ))
            category_news.append(d)
        
        news_dict[category] = category_news

    return news_dict    

def scrape_sources():
    sites = "jagran,oneindia,jansatta,navbharat,amarujala,ibn".split(',')
    sources_dict={}
    
    for site in sites:
        print site
        
        if site == "jagran":
            url1 = 'http://rss.jagran.com/rss/news/world.xml'
            url2 = 'http://rss.jagran.com/rss/news/national.xml'
            url3 = 'http://rss.jagran.com/rss/entertainment/bollywood.xml'
            url4 = 'http://rss.jagran.com/rss/josh/vigyan.xml'
            #TODO : add these dictionaries
            rss = feedparser.parse(url2)
            #rss = feedparser.parse(url1).items() + feedparser.parse(url2).items()#+feedparser.parse(url3).items()+ feedparser.parse(url4).items())
            #rss = Counter(feedparser.parse(url1)) +Counter(feedparser.parse(url2))

        elif site == 'oneindia':
            url = "http://news.oneindia.in/rss/news-india-fb.xml"
            rss = feedparser.parse(url)

        elif site == 'jansatta':
            url = "http://www.jansatta.com/feed/"
            rss = feedparser.parse(url)

        elif site == 'navbharat':
            url = "http://navbharattimes.indiatimes.com/rssfeedsdefault.cms"
            rss = feedparser.parse(url)

        elif site == 'amarujala':
            url = "http://www.amarujala.com/rss/editors-pick.xml"
            rss = feedparser.parse(url)

        elif site == 'ibn':
            url = "http://khabar.ibnlive.in.com/xml/top.xml"
            rss = feedparser.parse(url)

        sources_arr = []
        for item in rss['entries']:
            d= {}
            d['link'] = "https://www.instapaper.com/text?u="+item['link']
            d['title'] = item['title']
            d['description'] = item['description']
            d['image'] = get_image(item['description'])
            d['source'] = site
            d['title'] = item['title']
            date_object = string2date.parse(item['published'])
            date_object = date_object.replace(tzinfo=None)
            #date_object = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S GMT')
            d['date'] = pretty_date(date_object+timedelta( 0, 5*60*60 + 30*60 ))
            sources_arr.append(d)

        sources_dict[site]=sources_arr

    url = "http://aajtak.intoday.in.feedsportal.com/c/34152/f/618432/index.rss?option=com_rss&feed=RSS1.0&no_html=1&rsspage=home"
    rss = feedparser.parse(url)
    aajtak_arr =[]
    for item in rss['entries']:
        d= {}
        d['link'] = item['link']
        d['title'] = item['title']
        d['description'] = item['description']
        d['image'] = get_image(item['description'])
        d['source'] = site
        d['title'] = item['title']
        date_object = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S GMT')
        d['date']= pretty_date(date_object+timedelta( 0, 5*60*60 + 30*60 ))
        aajtak_arr.append(d)
        
    sources_dict['aajtak'] = aajtak_arr

    return sources_dict

def scrape_videos():
    channels = "ndtvindia,itvnewsindia,DDNewsofficial,abpnewstv,rajyasabhatv,bbchindi,zeenews".split(",")
    videos_dict = {}
    master_videos = []
    for author in channels:
        print author
        n=20
        videos = []
        inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?start-index=1&max-results={0}&alt=json&orderby=published&author={1}'.format( n, author ) )
        try:
            resp = json.load(inp)
            inp.close()
            returnedVideos = resp['feed']['entry']
            for video in returnedVideos:
                d= {}
                date = video['updated']['$t']
                date_object = string2date.parse(date)
                date_object = date_object.replace(tzinfo=None)
                d['date']= pretty_date(date_object+timedelta( 0, 5*60*60 + 30*60 ))
                d['epoch'] = date_object.strftime("%s")
                d['title'] = video['title']['$t']
                d['author'] = video['author'][0]['name']['$t']
                d['image'] = video['media$group']['media$thumbnail'][0]['url']
                d['description'] = video['media$group']['media$description']['$t']
                url = video['id']['$t']
                d['id'] = url.split('/')[-1]
                d['url'] = "http://www.youtube.com/embed/%s?autoplay=1"%d['id']
                print d['id']
                master_videos.append(d) 
                videos.append(d)
        except:
            #catch the case where the number of videos in the channel is a multiple of 50
            print "error"
            foundAll = True
            logging.exception('foo')

        videos_dict[author] = videos

    return videos_dict

with open("news.txt") as f:
    try:    news_json = json.loads(f.read())
    except: scrape_news()

@app.route('/refresh')
def refresh():
    
    with open('news.txt','w+') as f:
        f.write(json.dumps(scrape_news()))
    f.close()
    
    with open('sources_news.txt','w+') as f:
        f.write(json.dumps(scrape_sources()))
    f.close()
    
    with open('videos.txt','w+') as f:
        f.write(json.dumps(scrape_videos()))
    f.close()
    
    return "Done"


@app.route('/')
def index():
    return flask.redirect("/all")


@app.route('/<category>')
def catpage(category):
    #available categories ,w,n,b,e,s
    return flask.render_template('category.html',data=news_json[category])


@app.route('/sources')
def sopage():
    return flask.render_template('sources.html')

@app.route('/sources/<site>')
def so2page(site):
    with open("sources_news.txt") as f:
        arr = json.loads(f.read())

    return flask.render_template('category.html',data=arr[site])

@app.route('/videos')
def videos():
    with open("videos.txt") as f:
        arr = json.loads(f.read())
    f = []
    for key,value in arr.iteritems():
        f += value

    f = sorted(f, key=lambda k: k['epoch'],reverse=True) 

    return flask.render_template('videos.html',data=f)


@app.route('/about')
def aboutpage():
    return flask.render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)


