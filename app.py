import flask, flask.views
from flask import request
import os
import feedparser
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/<category>')
def catpage(category):
    #,w,n,b,e,s,h
    url = 'https://news.google.com/news/feeds?cf=all&hl=hi&output=rss&ned=hi_in&topic=%s'%(category)
    if category == "all":
        url = 'https://news.google.com/news/feeds?cf=all&hl=hi&output=rss&ned=hi_in'
    
    rss = feedparser.parse(url)
    arr =[]
    for item in rss['entries']:
        link = item['link']
        d= {}    
        #removing the google stuff from the url
        d['link'] = link[link.rfind('&url=')+5:]
        d['title'] = item['title']
        d['description'] = item['description']
        n = d['title'].rfind('-')
        d['source'] = d['title'][n+1: ]
        d['title'] = d['title'][:n]
        arr.append(d)
    
    return flask.render_template('category.html',data=arr,cat=category)

app.debug = True
app.run()
