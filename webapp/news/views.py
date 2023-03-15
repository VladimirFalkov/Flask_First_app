from flask import Blueprint, render_template
from webapp.news.models import News

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    title = 'Новости Питон'
    weather = {'temp_C': 11, 'FeelsLikeC':16 }
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list = news_list)