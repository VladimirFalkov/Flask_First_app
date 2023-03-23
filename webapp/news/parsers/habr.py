from datetime import datetime
from datetime import timedelta
import requests
import locale
import platform
from bs4 import BeautifulSoup
from webapp.db import db
from webapp.news.models import News

from webapp.news.parsers.utils import save_news, get_page


if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

def parse_habr_time(date_str):
       
    if 'сегодня' in date_str.lower():
        today = datetime.now()
        date_str = date_str.lower().replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str.lower():
        yestarday = datetime.now() - timedelta(days=1)
        date_str = date_str.lower().replace('вчера', yestarday.strftime('%d %B %Y'))
    try: 
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()
    


def get_python_habr_snippets():
    html = get_page("https://habr.com/ru/search/?q=python&target_type=posts&order=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_="tm-articles-list").findAll('article', class_="tm-articles-list__item")
        for news in all_news:
            title = news.find('h2').find('span').text
            url = 'https://habr.com' + news.find('a', class_="tm-article-snippet__title-link")['href']       
            published = news.find('time').text
            published = parse_habr_time(published)
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_page(news.url)
        if html:
           soup = BeautifulSoup(html, 'html.parser')
           news_text = soup.find('div', class_="pull-down").find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow").find('div',class_="tm-article-body").decode_contents()
           if news_text:
               news.text = news_text
               db.session.add(news)
               db.session.commit()