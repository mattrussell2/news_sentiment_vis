"""
db.py

Module used to run queries on database.
"""
import os
import MySQLdb
from queries import *

class DB:
    def __init__(self, db="news_vis"):
        #self.db = MySQLdb.connect(host="tcp://0.tcp.ngrok.io",
        #                          port="10326",#localhost",  # your host
        #                          user="matt",       # username
        #                          passwd=os.environ['DB_PW'],         # password
        #                          db=db)             # name of the database
        self.db = MySQLdb.connect(host="localhost",
                             port=3306,#localhost",  # your host
                             user="newz",       # username
                             passwd=os.environ['DB_PW'],         # password
                             db='news_vis')     
        self.db.cursor().execute('SET GLOBAL max_allowed_packet=500*1024*1024')
        self.db.set_character_set('utf8')
        self.db.cursor().execute('SET NAMES utf8')
        self.db.cursor().execute('SET CHARACTER SET utf8;')
        self.db.cursor().execute('SET character_set_connection=utf8;')

    def create_schema(self):
        cur = self.db.cursor()
        cur.execute(CREATE_TABLE_ENTITY)
        cur.execute(CREATE_TABLE_SOURCE)
        cur.execute(CREATE_TABLE_ARTICLE)
        cur.execute(CREATE_TABLE_MENTION)
        cur.execute(CREATE_FAVORITE_SOURCES)
        self.db.commit()


    def insert_sources_tuples(self, source_tuples):
        """
        Args:
        source_tuples: list of tuples the following form:

        (source_id, name, url, language, country, description, category)

        Inserts tuples into source table.
        """
        self.db.cursor().executemany(INSERT_SOURCE, source_tuples)
        self.db.commit()

    def insert_sources_dict(self, source_dict_list):
        """
        Args:
        source_dict_list: list of dicts of the following form

        [
            ...,
            {
                id: string,
                name: string,
                url: string,
                language: string,
                country: string,
                description: string,
                category: string
            },
            ...
        ]

        Inserts source objects into source table.
        """
        source_tuples = list(map(lambda object: (
                                    object['id'],
                                    object['name'],
                                    object['url'],
                                    object['language'],
                                    object['country'],
                                    object['description'],
                                    object['category']),
                                 source_dict_list))
        self.insert_sources_tuples(source_tuples)

    def insert_entities_tuples(self, entity_tuples):
        """
        Args:
        entity_tuples: list of tuples the following form:

        (entity_id, name, type, wikipedia_url, image,
         short_description, detailed_description, url)

        Inserts tuples into entity table.
        """
        self.db.cursor().executemany(INSERT_ENTITIES, entity_tuples)
        self.db.commit()

    def insert_articles_tuples(self, article_tuples):
        """
        Args:
        article_tuples: list of tuples the following form:

        (title, description, url, image_url, source_id,
         datetime_published, authors)

        Inserts tuples into article table.
        """
        self.db.cursor().executemany(INSERT_ARTICLES, article_tuples)
        self.db.commit()

    def insert_mentions_tuples(self, mention_tuples):
        """
        Args:
        mention_tuples: list of tuples the following form:

        (entity_id, name, article_title, source_id, datetime_published,
         sentiment_score, sentiment_magnitude, salience)

        Inserts tuples into mention table.
        """
        self.db.cursor().executemany(INSERT_MENTIONS, mention_tuples)
        self.db.commit()

# Tests
db = DB()


"""
db = DB(db="test")

db.insert_sources_dict([
    {
     'id': 'cnn',
     'name': 'CNN',
     'url': 'www.cnn.com',
     'language': 'en',
     'country': 'us',
     'description': 'Fake News.',
     'category': 'fake-news'
    },
    {
     'id': 'fox-news',
     'name': 'Fox News',
     'url': 'www.foxnews.com',
     'language': 'en',
     'country': 'us',
     'description': 'Real News.',
     'category': 'real-news'
     }])

db.insert_articles_tuples([
    ('title1',
     'description1',
     'url1',
     'image_url1',
     'cnn',
     'datetime_published1',
     'authors1'),
    ('title2',
     'description2',
     'url2',
     'image_url2',
     'fox-news',
     'datetime_published2',
     'authors2')
])

db.insert_entities_tuples([
    ('donald-trump',
     'Donal Trump',
     'Person',
     None,
     None,
     None,
     None,
     None),
    ('elon-musk',
     'Elon Musk',
     'Person',
     None,
     None,
     None,
     None,
     None)
])

db.insert_mentions_tuples([
    ('donald-trump',
     'Donal Trump',
     'title1',
     'cnn',
     'datetime_published1',
     -1,
     1,
     0.5),
    ('elon-musk',
     'Elon Musk',
     'title2',
     'fox-news',
     'datetime_published2',
     1,
     1,
     0.3)
])"""
