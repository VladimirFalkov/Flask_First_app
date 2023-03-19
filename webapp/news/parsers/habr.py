from datetime import datetime
import requests
from bs4 import BeautifulSoup
from flask import current_app
from webapp.db import db
from webapp.news.models import News

from webapp.news.parsers.utils import save_news, get_page


def get_python_habr_snippets():
    html = get_page("https://habr.com/ru/search/?q=python&target_type=posts&order=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_="tm-articles-list").findAll('article', class_="tm-articles-list__item")
        for news in all_news:
            title = news.find('h2').find('span').text
            url = 'https://habr.com' + news.find('a', class_="tm-article-snippet__title-link")['href']       
            published = news.find('time').text
            
            print(title)
            print(url)
            print(published)
            print('-------------------------------------------')
            
            """try:
                published = datetime.strptime(published, "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)"""