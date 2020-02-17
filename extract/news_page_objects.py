import bs4
import requests

from common import config


class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)  # despues de visitar la pagina ahora tiene el arbol del sitio

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()  # esto va a levantar un error si la solicitud no termino bien

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):
    # news_site_uid {xataka, enter.co}, url {https://www.xataka.com/, https://www.enter.co/}
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property  # hace que se pueda acceder a una metodo como un atributo
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):  # gracias a que heredamos de un objeto padre tenemos todas sus propiedades
        super().__init__(news_site_uid, url)  # scrapear el sitio esta implicito

    @property
    def body(self):
        # como somos una instancia, extención, del objeto NewsPage podemos utilizar el metodo _select
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''

    @property
    def url(self):
        return self._url
