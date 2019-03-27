from app import create_app
from config import config, Config

app = create_app(config['development'])

@app.route('/')
def index():
  """Default app home page"""

  return 'Welcome to News summarizer!'


if __name__ == "__main__":
    app.run()
