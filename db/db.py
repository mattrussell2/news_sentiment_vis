"""
db.py

Module used to run queries on database.
"""
import os
import MySQLdb
from queries import *

class DB:
    def __init__(self, db="news_vis", local=False):
        if local:
            self.db = MySQLdb.connect(host="localhost",
                                      #user='root',
                                      #passwd=os.environ['DB_PW'],
                                      db=db,
                                      user="root",
            )
        else:
            self.db = MySQLdb.connect(host="tcp://0.tcp.ngrok.io",
                                      port="10326",
                                      user="matt",
                                      passwd=os.environ['DB_PW'],
                                      db=db)
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

    def get_top_entities(self, count):
        cur = self.db.cursor()
        cur.execute(GET_TOP_MENTIONS_COUNT_ALL.format(count))
        result = [{"entity_id": row[0],
                   "name": row[1],
                   "count": row[2]} for row in cur.fetchall()]
        return result

    def get_sources(self):
        cur = self.db.cursor()
        cur.execute(GET_SOURCES)
        result = [{"source_id": row[0],
                 "name": row[1]} for row in cur.fetchall()]
        return result

    def get_entity_sentiment(self, entities, sources):
        """
        {"Trump" :
            {"total_info" : [
                    {"source" : "",
                     "positive" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "neutral" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "negative" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "mentioned_with" : [],
                     "article_count" : 1,
                     "article_total" : 1
                    }
                ],
                "date_info" : []
            }
        }
        """
        result = {}
        cur = self.db.cursor()
        for entity in entities:
            name = entity["name"]
            entity_id = entity["entity_id"]
            result[name] = {"total_info" : [],
                            "date_info" : []}
            for source in sources:
                source_id = source["source_id"]
                object = {"source" : {"source_id" : source_id,
                                      "name" : source["name"]}}

                cur.execute(POS_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
                row = cur.fetchall()[0]
                print("pos_row")
                print(row)
                object["positive"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                                      "count" : row[2]}
                #print(row[0] * row[1])
                print(object["positive"]["sentiment"])

                cur.execute(NEG_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
                row = cur.fetchall()[0]
                object["negative"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                                      "count" : row[2]}

                cur.execute(NEUTRAL_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
                row = cur.fetchall()[0]
                object["neutral"] = {"sentiment" : row[0],
                                      "count" : row[1]}

                cur.execute(GET_TOP_MENTIONED_WITH_COUNT.format(entity_id, source_id, 10))
                object["mentioned_with"] = []
                for row in cur.fetchall():
                    object["mentioned_with"].append({"entity_id" : row[0], "name": row[1]})

                object["article_count"] = object["positive"]["count"] + object["negative"]["count"] + object["neutral"]["count"]

                cur.execute(GET_TOTAL_ARTICLES_FROM_SOURCE.format(source_id))
                object["article_total"] = cur.fetchall()[0]

                result[name]["total_info"].append(object)

        return result



    def non_time_entity_sentiment_one_source_one_id(self,entity_id,source,cur):
        source_id = source["source_id"]
        object = {"source" : {"source_id" : source_id,
                              "name" : source["name"]}}

        cur.execute(POS_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
        row = cur.fetchall()[0]
        print("pos_row")
        print(row)
        object["positive"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                              "count" : row[2]}
        #print(row[0] * row[1])
        print(object["positive"]["sentiment"])

        cur.execute(NEG_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
        row = cur.fetchall()[0]
        object["negative"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                              "count" : row[2]}

        cur.execute(NEUTRAL_SENTIMENT_BY_SOURCE_AND_ENTITY.format(entity_id, source_id))
        row = cur.fetchall()[0]
        object["neutral"] = {"sentiment" : row[0],
                             "count" : row[1]}

        cur.execute(GET_TOP_MENTIONED_WITH_COUNT.format(entity_id, source_id, 10))
        object["mentioned_with"] = []
        for row in cur.fetchall():
            object["mentioned_with"].append({"entity_id" : row[0], "name": row[1]})

        object["article_count"] = object["positive"]["count"] + object["negative"]["count"] + object["neutral"]["count"]

        cur.execute(GET_TOTAL_ARTICLES_FROM_SOURCE.format(source_id))
        object["article_total"] = cur.fetchall()[0]

        return object

    def get_entity_sentiment_with_time(self, entities, sources):
        """
        {"Trump" :
            {"total_info" : [
                    {"source" : "",
                     "positive" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "neutral" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "negative" : {
                        "sentiment" : 1,
                        "count" : 1
                     },
                     "mentioned_with" : [],
                     "article_count" : 1,
                     "article_total" : 1
                    }
                ],
                "date_info" : [ {date: 2018_11_14:},
                                {"source" : "",
                                 "positive" : {
                                    "sentiment" : 1,
                                    "count" : 1
                                },
                                "neutral" : {
                                    "sentiment" : 1,
                                    "count" : 1
                                },
                                "negative" : {
                                    "sentiment" : 1,
                                    "count" : 1
                                },
                                "mentioned_with" : [],
                                "article_count" : 1,
                                "article_total" : 1
                                }
                              ]
            }
        }
        """
        result = {}
        cur = self.db.cursor()
        for entity in entities:
            name = entity["name"]
            entity_id = entity["entity_id"]
            result[name] = {"total_info" : [],
                            "date_info" : []}

            #first deal with total info
            for source in sources:
                result[name]['total_info'].append(self.non_time_entity_sentiment_one_source_one_id(entity_id,source,cur))

            #now deal with date version
            dates = ['2018-11-'+ str(x) for x in range(14,23)]
            for date,i in zip(dates,range(len(dates))):

                result[name]['date_info'].append({'date': date, 'daily_info':[]})

                for source in sources:
                    source_id = source["source_id"]
                    object = {"source" : {"source_id" : source_id,
                                          "name" : source["name"]}}

                    cur.execute(POS_SENTIMENT_BY_SOURCE_AND_ENTITY_AND_DATE.format(entity_id, source_id,date))
                    row = cur.fetchall()[0]
                    print("pos_row")
                    print(row)
                    object["positive"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                                        "count" : row[2]}
                    #print(row[0] * row[1])
                    print(object["positive"]["sentiment"])

                    cur.execute(NEG_SENTIMENT_BY_SOURCE_AND_ENTITY_AND_DATE.format(entity_id, source_id,date))
                    row = cur.fetchall()[0]
                    object["negative"] = {"sentiment" : row[0] * row[1] if row[0] and row[1] else 0,
                                          "count" : row[2]}

                    cur.execute(NEUTRAL_SENTIMENT_BY_SOURCE_AND_ENTITY_AND_DATE.format(entity_id, source_id,date))
                    row = cur.fetchall()[0]
                    object["neutral"] = {"sentiment" : row[0],
                                         "count" : row[1]}

                    cur.execute(GET_TOP_MENTIONED_WITH_COUNT_AND_DATE.format(entity_id, source_id, date, 10))
                    object["mentioned_with"] = []
                    for row in cur.fetchall():
                        object["mentioned_with"].append({"entity_id" : row[0], "name": row[1]})

                    object["article_count"] = object["positive"]["count"] + object["negative"]["count"] + object["neutral"]["count"]

                    cur.execute(GET_TOTAL_ARTICLES_FROM_SOURCE_BY_DATE.format(source_id,date))
                    object["article_total"] = cur.fetchall()[0]

                    result[name]['date_info'][i]['daily_info'].append(object)

        return result




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
