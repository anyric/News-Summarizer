from app import create_app
from config import config, Config
from app.urls import getArticleURLS

app = create_app(config['development'])
main_url = 'https://www.monitor.co.ug'
news_url = 'https://www.monitor.co.ug/News/688324-688324-156c2gl/index.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
base_url = [main_url, news_url]


@app.route('/')
def index():
  """Default app home page"""

  return 'Welcome to News summarizer!'
@app.route('/urls')
def get_urls():
  """Get all headline urls from site base url"""
  urls_list = getArticleURLS(base_url,headers)

  return urls_list

if __name__ == "__main__":
    app.run()
