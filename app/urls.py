import requests
import time
import json
import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup

def getArticleURLS(base_url, headers):
    """Scrape monitor website for news headlines urls.
    
    Arguments:
        url: The url of the homepage to scrap headline  urls from
        
    Return:
        list: The list of urls for monitor news headline
    """
    
    url_links = []
    for url in base_url:
        try:
            #retrieve webpage from the url
            page = requests.get(url, headers=headers).text

            #use beautifulSoup to scrap the page
            soup = BeautifulSoup(page, 'lxml')

            links = []
            #loop through the page to collect anchor tags and retrieve the urls
            for a in soup.find_all(href=True):
              links.append(a['href'])
              # titles.append(a.text.encode('ascii',errors='replace').replace(b'?', b' ').decode('utf8'))

            #clean collected urls
            final_links = [link for link in links if '/News/' in link]
            clean_links = [link for link in final_links if not 'News/688334-688334' in link]
            clean_urls = ['https://www.monitor.co.ug' + link for link in clean_links if not 'https://www.monitor.co.ug' in link]
            cleaned_links = list(OrderedDict.fromkeys(clean_urls))
            url_links += cleaned_links
            time.sleep(2)
        except requests.exceptions.ConnectionError as error:
            return error

    #patterns to filter base urls with headlines only
    patterns = ['/News/688324-','/News/National/688334-','/News/Education/688336-',
                '/News/Insight/688338-','/News/World/688340-','/News/photos/3286528-']
    result_list = [row for row in url_links if not any(p in row for p in patterns)]

    return result_list