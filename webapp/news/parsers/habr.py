from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import platform
from webapp.news.parsers.utils import get_html, save_news, get_news_content

# print(locale.getlocale())
# if platform.system() == 'Windows':
#     locale.setlocale(locale.LC_ALL, 'russian')
# else:
#     locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


def get_habr_snippets():
    html = get_html('https://habr.com/ru/search/?target_type=posts&q=python&order_by=date')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='content-list_posts').find_all('li', class_='content-list__item_post')
        result_news = []
        for news in all_news:
            title = news.find('a', class_='post__title_link').text
            url = news.find('a', class_='post__title_link')['href']
            published = parse_habr_date(news.find('span', class_='post__time').text)
            # print(title, url, published)
            save_news(title, url, published)
            get_news_content()


def parse_habr_date(date_str):
    # print(date_str)
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    # print(date_str)
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
        # return date_str
    except ValueError:
        # print('была ошибка')
        return datetime.now()



