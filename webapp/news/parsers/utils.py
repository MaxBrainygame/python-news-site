import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent': generate_user_agent(os='linux')
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    # print(not news_exists)
    if not news_exists:
        news_news = News(title=title, url=url, published=published)
        # print(news_news)
        db.session.add(news_news)
        db.session.commit()


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find('div', class_='post__text-html').decode_contents()
            if article:
                news.text = article
                db.session.add(news)
                db.session.commit()
