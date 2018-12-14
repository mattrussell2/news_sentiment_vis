import os
import pickle
import json
from data_processing import *

article_rows_file = open("temp/article_rows.json", "w")
entity_rows_file = open("temp/entity_rows.json", "w")
mention_rows_file = open("temp/mention_rows.json", "w")
source_rows_file = open("temp/source_rows.json", "w")

article_rows = []
entity_rows = []
mention_rows = []
source_rows = []

for news_org in os.listdir('articles_sentiment'):
    print(news_org)
    for one_day in os.listdir('articles_sentiment/'+news_org):
        print(one_day)

        fstr = 'articles_sentiment/' + news_org + '/' + one_day
        f = open(fstr,'rb')
        one_day_articles = pickle.load(f)

        for article in one_day_articles:
            if 'IBM_sentiment' in article.keys() and \
               'GOOGLE_sentiment' in article.keys():

                article_rows.append(article_row_from_article_object(article))
                mention_rows.extend(mention_rows_from_article_object(article))
                entity_rows.extend(entity_rows_from_article_object(article))
                source_rows.append(source_row_from_article_object(article))

json.dump(article_rows, article_rows_file)
json.dump(entity_rows, entity_rows_file)
json.dump(mention_rows, mention_rows_file)
json.dump(source_rows, source_rows_file)
