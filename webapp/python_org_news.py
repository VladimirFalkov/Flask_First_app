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
    html = get_page(current_app.config('URL_FOR_NEWS'))
    if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_news = soup.find('ul', class_="list-recent-posts menu").findAll('li')
            result_news = []
            for news in all_news:
                title = news.find('a').text
                url = news.find('a')['href']
                published = news.find('time').text
                try:
                    published = datetime.strptime(published,' %Y-%m-%d')
                except ValueError:
                     puplished = datetime.now()
                save_news(title, url, published)
    return False   


def save_news(title, url, published):
     news_news = News(title=title, url=url, published=published)
     db.session.add(news_news)
     db.session.commit()