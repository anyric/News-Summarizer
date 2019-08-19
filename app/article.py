import os
import time
import requests
import json
from datetime import date
from bs4 import BeautifulSoup
from app.urls import getArticleURLS
import pandas as pd

data = pd.DataFrame()

def getArticle(url, headers,image_name):
    """Scrape monitor website url for data.
    
    Arguments:
        url: The url of the webpage to be scrap for data
        
    Return:
        text: The string article scraped from the webpage
    """

    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'lxml')
    
    article = soup.select('section.body-copy > div > p')
    title = soup.title.text.encode('ascii',errors='replace').replace(b'?', b' ').decode('utf8')
    imgs = soup.findAll("img", {"class":"photo_article"})
    img_name = './app/static/img-'+ str(date.today()) +'/' + image_name + '.png'
    post = ""

    if not os.path.isdir('./app/static/img-' + str(date.today())):
        path = './app/static/img-' + str(date.today())
        os.mkdir(path)

    for p in article:
        post += p.getText()

    for img in imgs:
        time.sleep(2)
        im_url = 'https://www.monitor.co.ug' + img.get('src')
        image = requests.get(im_url,headers=headers)
        open(img_name,'wb').write(image.content)
    image = '/static/img-'+ str(date.today()) +'/' + image_name + '.png'

    return title, post, url, image

def getMonitorArticles(links, headers):
    """Scrape monitor website articles for links.
    
    Arguments:
        urls: The list of urls of the webpage to be scrap for data
        
    Return:
        list: The list of string articles scraped from the webpages
    """
    
    titles = []
    articles = []
    urls = []
    img_name = 'post1'
    images = []
    post = 0
    for link in links:
        img_name = 'post' + str(post)
        post += 1
        title, article, url ,img = getArticle(link, headers, img_name)
        if not title in titles:
            titles.append(title)
            articles.append(article)
            urls.append(url)
            images.append(img)
        
    data['Titles'] = titles
    data['Articles'] = articles
    data['Urls']=urls
    data['Images'] = images

    return data

def getAllArticles(base_url,headers):
    """Get all articles from given base url"""
    
    links = getArticleURLS(base_url,headers)
    time.sleep(1)

    if isinstance(links, list):
        posts = getMonitorArticles(links,headers)
        posts = posts.drop_duplicates(['Titles','Images'], keep='first')
        posts.to_csv("./app/databases/posts-" + str(date.today()) + ".csv")
    else:
      time.sleep(3)
      getAllArticles(base_url,headers)
    
    return
