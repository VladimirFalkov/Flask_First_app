import requests
from webapp.db import db
from webapp.news.models import News


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/201'
}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False
    

# This function saved news in DB
def save_news(title, url, published):
    # Lets check if news is new and if it is - add it to DB
    news_exist = News.query.filter(News.url==url).count()
    if not news_exist:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()