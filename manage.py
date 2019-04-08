import os
import requests
import json
import time
from datetime import date
import pandas as pd
from flask import render_template, request, redirect
from app import create_app
from config import config, Config
from app.urls import getArticleURLS
from app.article import getMonitorArticles, getAllArticles
from app.clean_text import normalizeText
from app.summary import frequencyDistributionTextSummarizer, lsaTextSummarizer, textRankTextSummarizer
from app.cluster import classifyArticles

app = create_app(config['development'])
main_url = 'https://www.monitor.co.ug'
news_url = 'https://www.monitor.co.ug/News/688324-688324-156c2gl/index.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
base_url = [main_url, news_url]
urls = pd.DataFrame()
data = pd.DataFrame()

@app.route('/', methods=['GET'])
def index():
    """Default app home page displaying summary articles"""
    if os.path.isfile('./app/databases/posts-' + str(date.today()) + '.csv'):
      normalized = pd.read_csv("./app/databases/posts-" + str(date.today()) + ".csv")
    elif os.path.isfile('./app/databases/posts-2019-04-17.csv'):
      normalized = pd.read_csv("./app/databases/posts-2019-04-17.csv")
      normalized = normalized.drop_duplicates('Titles', keep='first')
    else:
      getAllArticles(base_url,headers)
      normalized = pd.read_csv("./app/databases/posts-" + str(date.today()) + ".csv")
    normalized = normalized.dropna()
    normalized_text = normalizeText(normalized["Articles"])

    summarized_text = textRankTextSummarizer(normalized_text, 3)
    data['Id'] = normalized['Unnamed: 0']
    data['Titles'] = normalized['Titles'].apply(lambda title: title.replace('- Daily Monitor', ' '))
    data['Articles'] = normalized['Articles'].apply(lambda article: article.replace('[email protected]', ' '))
    data['Summaries'] = summarized_text
    data['Urls'] = normalized['Urls']
    data['Images'] = normalized['Images']
    cluster = classifyArticles(data['Summaries'])
    data['Cluster'] = cluster
    articles= data.sort_values(by=['Cluster'])
  
    return render_template('index.html', data=articles)

@app.route('/summarizer', methods=['POST','GET'])
def compare():
    """Default app home page displaying summary articles"""
    if request.method == 'POST':
        model = request.form['model']
        post = request.form['post'].replace('?', ' ')
        posts = normalizeText([post])

        if model == 'summariseArtcle':
          summarized_text = frequencyDistributionTextSummarizer(posts, 3)
        elif model == 'lsaTextSummarizer':
          summarized_text = lsaTextSummarizer(posts, 3)
        elif model == 'textRankSummarizer':
          summarized_text = textRankTextSummarizer(posts, 3)

        posts = {"Original": post, "Summary": summarized_text}
    
        return render_template('summarizer.html', posts=posts)
    posts = {"Original": None, "Summary": None}
    return render_template('summarizer.html', posts=posts)

@app.route('/urls')
def get_urls():
  """Get all headline urls from site base url"""

  urls_list = getArticleURLS(base_url,headers)
  urls["Urls"] = urls_list
  return json.dumps(urls_list)

@app.route('/article/<id>', methods=['GET'])
def get_summary(id):
    """Gets an article based on the id """
    index = int(id)

    if len(data) < 1:
      return redirect('/',code=302)

    article = data.loc[index]

    return render_template('compare.html', data=article)

@app.route('/about', methods=['GET'])
def about():
    """Describes Todoy inBrief """
    
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
