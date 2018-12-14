from flask import Flask, request, session
from flask_cors import CORS
import json
import sys
import os
sys.path.append('/home/matt/177/vis/')
import MySQLdb
sys.path.append('/home/matt/177/db/')
from queries import *

#setup connection to database
db = MySQLdb.connect(host="localhost",
                     port=3306,#localhost",  # your host
                     user="newz",       # username
                     passwd=os.environ['DB_PW'],         # password
                     db='news_vis')             # name of the database
cursor = db.cursor()
cursor.execute("SELECT * FROM mention;")#"SELECT * FROM mention")
i=0
for row in cursor.fetchall():
    print row
    i+=1
    if i>5: exit()

    #"SELECT name FROM mention WHERE NOT NULL;"
