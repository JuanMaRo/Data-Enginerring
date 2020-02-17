import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from article import Article
from base import Base, engine, Session


logger = logging.getLogger(__name__)


def main(filename):
    Base.metadata.create_all(engine)  # nos genera el schema
    session = Session()
    articles = pd.read_csv(filename)  # genera un dataframe, es un dataframe

    for index, row in articles.iterrows():  # nos da el indice y la columna
        logger.info('Loading article uid {} into DB'.format(row['uid']))
        article = Article(row['uid'],  # le pasamos cada uno de los valores al constructor
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_tokens_body'],
                          row['n_tokens_title'],
                          row['title'],
                          row['url'])

        session.add(article)  # Esto ya esta metiendo nuestro articulo en la base de datos

    session.commit()
    session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The file you want to load into the db',
                        type=str)

    args = parser.parse_args()

    main(args.filename)