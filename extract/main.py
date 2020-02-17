import argparse  # libreria para crear un CLI
import csv
import datetime
import logging  # es una forma mas bonita de arrojar resultados en consola
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config


logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')  # https://example.com/hello
is_root_path = re.compile(r'^/.+$')  # /some-text


def _news_scraper(news_site_uid):  # news_site_uid porque estamos utilizando las llaves como IDs {xataka, enter.co}
    host = config()['news_sites'][news_site_uid]['url']  # {https://www.xataka.com/, https://www.enter.co/}

    logging.info('Beginning scraper for {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)  # contiene un set con los links del homepage

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('Article fetched!!')
            articles.append(article)
            #break  # hace que se rompa el ciclo solamente cuando tengamos el primer articulo

    _save_articles(news_site_uid, articles)


def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=now
    )
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

    # garantiza que tengamos todas las propiedades del objeto ArticlePage, no importa que luego sea modificado
        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            # esto es un codigo robusto
            writer.writerow(row)


def _fetch_article(news_site_uid, host, link):
    logger.info('Start fetching article at {}'.format(link))

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # news_site_choices es un iterable
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()  # parsea nuestros argumentos y nos devolvera un objeto con ellos
    _news_scraper(args.news_site)
