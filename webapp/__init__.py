from flask import Flask, render_template
from flask_login import LoginManager
from webapp.model import db, News
from webapp.forms import LoginForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    @app.route('/')
    def index():
        title = 'Новости Питон'
        weather = {'temp_C': 11, 'FeelsLikeC':16 }
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list = news_list)
    
    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    
    return app