from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import current_app
from webapp.model import db, News

def get_page(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False
    
def get_python_news():
    html = get_page("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_="list-recent-posts menu").findAll('li')
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']       
            published = news.find('time').text
            try:
                published = datetime.strptime(published, "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)

# This function saved news in DB
def save_news(title, url, published):
    # Lets check if news is new and if it is - add it to DB
    news_exist = News.query.filter(News.url==url).count()
    if not news_exist:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()
        