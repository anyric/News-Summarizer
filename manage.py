import json
import time
import pandas as pd
from app import create_app
from config import config, Config
from app.urls import getArticleURLS
from app.article import getMonitorArticles

app = create_app(config['development'])
main_url = 'https://www.monitor.co.ug'
news_url = 'https://www.monitor.co.ug/News/688324-688324-156c2gl/index.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
base_url = [main_url, news_url]
urls = pd.DataFrame()
data = pd.DataFrame()

@app.route('/')
def index():
  """Default app home page"""

  return 'Welcome to News summarizer!'
@app.route('/urls')
def get_urls():
  """Get all headline urls from site base url"""

  urls_list = getArticleURLS(base_url,headers)
  urls["Urls"] = urls_list
  return json.dumps(urls_list)

@app.route('/articles')
def get_articles():
  """Get all articles from given base url"""

  links = getArticleURLS(base_url,headers)
  time.sleep(2)
  articles = getMonitorArticles(links,headers)

  data["Titles"] = articles[0]
  data["Articles"] = articles[1]
  data["Urls"] = articles[2]
  # data.to_csv("./articles.csv")
  return articles


if __name__ == "__main__":
    app.run()
