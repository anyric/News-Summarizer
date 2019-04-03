import requests
import json
from bs4 import BeautifulSoup
from app.urls import getArticleURLS

def getArticle(url, headers):
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
    post = ""

    for p in article:
        post += "".join(p.text.encode('ascii',errors='replace').replace(b'?', b' ').decode('utf8'))
    
    return title, post, url

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
    for link in links:
        title, article, url = getArticle(link, headers)
        titles.append(title)
        articles.append(article)
        urls.append(url)
    
    return json.dumps({"Titles":titles, "Articles":articles, "Urls":links})
