"""
data_extraction.py

Query database to create json file for visualization
"""

import json
import sys
sys.path.append("db")
from db import *
from queries import *

def dump_top_entities():
    db = DB(local=True)
    result = []
    for entity in db.get_top_entities(500):
        result.append(entity)

    json.dump(result, open("top500_entities.json", "w"))

def dump_sources():
    db = DB(local=True)
    json.dump(db.get_sources(), open("sources.json", "w"))

def dump_entity_sentiment(n):
    sources = json.load(open("sources.json", "r"))
    entities = json.load(open("top{}_entities.json".format(n), "r"))

    db = DB(local=True)
    json.dump(db.get_entity_sentiment_with_time(entities, sources), open("dataset_with_time.json", "w"))

dump_top_entities()
dump_entity_sentiment(500)
