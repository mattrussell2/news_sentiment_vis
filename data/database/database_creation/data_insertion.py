"""
data_insertion.py

Insert data into the database from json rows
"""
import json
import sys
sys.path.append("db")
from db import *

article_rows_file = open("temp/article_rows.json", "r")
mention_rows_file = open("temp/mention_rows.json", "r")
entity_rows_file = open("temp/entity_rows.json", "r")
source_rows_file = open("temp/source_rows.json", "r")

print("Files opened")

#article_rows = json.load(article_rows_file)
mention_rows = json.load(mention_rows_file)
entity_rows = json.load(entity_rows_file)
print(entity_rows[0])
print(mention_rows[0])
exit()

mention_rows = [[x.encode('utf-8') if type(x)==unicode else x for x in article] for article in mention_rows]

print(type(mention_rows[0][1]))
exit()

entity_rows = json.load(entity_rows_file)
source_rows = json.load(source_rows_file)

print("Json loaded")


article_rows = [[x.encode('utf-8') if type(x)==unicode else x for x in article] for article in article_rows]
mention_rows = [[x.encode('utf-8') if type(x)==unicode else x for x in article] for article in mention_rows]
entity_rows =  [[x.encode('utf-8') if type(x)==unicode else x for x in article] for article in entity_rows]
source_rows =  [[x.encode('utf-8') if type(x)==unicode else x for x in article] for article in source_rows]

article_tuples = [tuple(x) for x in article_rows]
mention_tuples = [tuple(x) for x in mention_rows]
entity_tuples = [tuple(x) for x in entity_rows]
source_tuples = [tuple(x) for x in source_rows]

print("Tupleified")

database = DB()

database.insert_sources_tuples(source_tuples)
print("Inserted sources")
database.insert_articles_tuples(article_tuples)
print("Inserted articles")
database.insert_entities_tuples(entity_tuples)
print("Inserted entities")
database.insert_mentions_tuples(mention_tuples)
print("Inserted mentions")
