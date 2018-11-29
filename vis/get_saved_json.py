from flask import Flask, request, session
from flask_cors import CORS
import json
import sys
import os
sys.path.append('/home/matt/177/vis/')
import MySQLdb
sys.path.append('/home/matt/177/db/')
from queries import *
import math


import numpy as np

news_orgs = ['abc-news', 'buzzfeed', 'cnn', 'nbc-news', 'the-new-york-times', 'bbc-news', 'cbc-news',
'financial-times', 'politico', 'the-wall-street-journal', 'breitbart-news', 'cbs-news', 'fox-news', 'the-economist', 'the-washington-post', 'business-insider', 'cnbc', 'msnbc', 'the-huffington-post', 'usa-today']
news_orgs.sort()

short_labels = ['ABC','BBC','BBN','BI','BZFD','CBC','CBS','CNBC','CNN','FT','FOX','MSNBC','NBC','POL','ECON','HUFF','NYT','WSJ','WASH','USA']

#setup connection to database
db = MySQLdb.connect(host="localhost",
                     port=3306,#localhost",  # your host
                     user="newz",       # username
                     passwd=os.environ['DB_PW'],         # password
                     db='news_vis')             # name of the database
cursor = db.cursor()


def hola():
    reqs = ['Donald Trump','Jamal Khashoggi','Lettuce']#request.form.to_dict()   
    org_values = {}
    final_results = {}
    for req in reqs:
        for org in news_orgs:
            print("STRING: \n" + "SELECT sentiment_score,sentiment_magnitude from mention where name='"+req+"' and source_id='"+org +"';")
            cursor.execute("SELECT sentiment_score,sentiment_magnitude from mention where name='"+req+"' and source_id='"+org +"';")# limit 100;")
            org_values[org] = []      
            org_values[org] = [[y for y in x]  for x in cursor.fetchall()]
            if org_values[org] == []:
                org_values.pop(org)

            labels = ['positive','negative','neutral']
        all_values = {short_labels[news_orgs.index(org)]:{label:[] for label in labels} for org in org_values.keys()}
        for org in org_values.keys():
            for article in org_values[org]:           
                score = article[0]
                magnitude = article[1]
            
                if score == 0: adjusted_score = magnitude #add magnitude for 0 score vals
                else: adjusted_score = score * magnitude

                adjusted_label = short_labels[news_orgs.index(org)]
                    
                if score > 0:
                    all_values[adjusted_label]['positive'].append(adjusted_score)
                if score < 0:
                    all_values[adjusted_label]['negative'].append(adjusted_score)
                if score == 0:
                    all_values[adjusted_label]['neutral'].append(adjusted_score)

            #determine averages
        totals = {org:{label:np.mean(all_values[org][label]) for label in labels} for org in all_values.keys()}
            #impute nan values
        totals = {org:{label: totals[org][label] if not math.isnan(totals[org][label]) else 0 for label in labels} for org in all_values.keys()}

        final_results[req] = totals

    f = open('testing_output.json','w')
    json.dump(final_results,f)

    #now sorted by sentiment, magnitude, score, for each news organization  
#    values = json.dumps(totals)


def view_saved():

    f = open('testing_output.json','r')
    input = json.load(f)
    print(input.keys())
    for key in input.keys():
        print(input[key])
        exit()

view_saved()
#hola()
