import os
import requests
import json
import time
import nltk
from datetime import date, timedelta
from apscheduler.scheduler import Scheduler
from apscheduler.events import EVENT_JOB_ERROR
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
nltk.download('punkt')
urls = pd.DataFrame()
data = pd.DataFrame()
sched = Scheduler(daemon=True)
sched.start()
img =[]
today = date.today()
yesterday = today - timedelta(days = 1)

@app.route('/', methods=['GET'])
def loader():
    """Todoy inBrief page loader """
    cron_job()
    return render_template('temp.html', title="Loader")

@app.route('/index', methods=['GET'])
def index():
    """Default app home page displaying summary articles"""
    
    if os.path.isfile('./app/databases/posts-' + str(today) + '.csv'):
        normalized = pd.read_csv("./app/databases/posts-" + str(today) + ".csv")
        normalized = normalized.drop_duplicates('Titles', keep='first')
        img.append('/static/img-' + str(today))
    elif os.path.isfile('./app/databases/posts-' + str(yesterday) + '.csv'):
        normalized = pd.read_csv("./app/databases/posts-" + str(yesterday) + ".csv")
        normalized = normalized.drop_duplicates('Titles', keep='first')
        img.append('/static/img-' + str(yesterday))
    else:
      return render_template('temp.html', title="Loader")

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
    
    img.append(data.loc[0:2]['Titles'][0])
    img.append(data.loc[0:2]['Titles'][1])
    img.append(data.loc[0:2]['Titles'][2])
    return render_template('index.html', data=articles, image=img, title="Home")

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
    return render_template('summarizer.html', posts=posts, title="Summarizer")

@app.route('/article/<int:id>', methods=['GET'])
def get_summary(id):
    """Gets an article based on the id """

    if len(data) < 1:
      return redirect('/index',code=302)

    article = data.loc[id]

    return render_template('compare.html', data=article, title="Article")

@app.route('/about', methods=['GET'])
def about():
    """Describes Todoy inBrief """
    
    return render_template('about.html', title="About")

@sched.interval_schedule(seconds=5)
def cron_job():
  if not os.path.isfile('./app/databases/posts-' + str(today) + '.csv'):
    getAllArticles(base_url,headers)

def job_listener(event):
    if event.exception:
        time.sleep(3)
        cron_job()

if __name__ == "__main__":
    app.run()
