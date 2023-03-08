from flask import Flask, render_template
from webapp.python_org_news import get_python_news
from webapp.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    @app.route('/')
    def index():
        title = 'Новости Питон'
        weather = {'temp_C': 11, 'FeelsLikeC':16 }
        news_list = get_python_news()
        return render_template('index.html', page_title=title, weather=weather, news_list = news_list)

    return app