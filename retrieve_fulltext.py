import json
import os
from newspaper import Article
import requests
from datetime import datetime

#this script iterates over all the files stored in articles_newsapi/, and for each file
#will create a corresponding file in articles_fulltext/ that contains the same content
#(array of dictionaries, one per news article), except each dictionary also contains the fulltext
#of each article as a key/value pair, accessible by articles[i]['fulltext']

#get the fulltext using newspaper3k
def get_fulltext(url):   
    try:
        article = Article(url)       
        article.download()
        article.parse()
        return article.text
    except:      
        return 'bad url'

#keep track of the time
start = datetime.now()

#for all news orgs 
for news_org in os.listdir('articles_newsapi'):        
    print(news_org)

    #make sure the path exists to save the file
    if not os.path.exists('articles_fulltext/' + news_org):
       os.mkdir('articles_fulltext/' + news_org)   

    #iterate over all the files (each day) for that given news org
    for one_day in os.listdir('articles_newsapi/'+news_org):

        #if we already have fulltext of that day, skip the file
        if one_day in os.listdir('articles_fulltext/' + news_org + '/'):
            continue

        print(one_day)
          
        #load all articles for the given day
        fstr = 'articles_newsapi/' + news_org + '/' + one_day
        f = open(fstr)            
        articles = json.load(f)['articles'] #json.load(infile)
        print('num articles: ' + str(len(articles)))

        #array to keep track of all articles for one day for one news org, with fulltext
        all_with_fulltext = []

        #for each article in the day
        for i in range(len(articles)):

            #print article number if divisible by 10
            if i % 10 == 0: print('article #' + str(i))           

            #add fulltext to the article
            article = articles[i]
            article['fulltext'] = get_fulltext(article['url'])

            #save the article, now with fulltext
            all_with_fulltext.append(article)

        #save the file    
        with open('articles_fulltext/' + news_org + '/' + one_day,'w') as outfile:
            json.dump(all_with_fulltext,outfile)

print ("it has taken: " + str(datetime.now()-start))
