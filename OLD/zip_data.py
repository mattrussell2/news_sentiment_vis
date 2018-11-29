import json
import pickle
import os
import re
import requests
from datetime import datetime
from difflib import SequenceMatcher

start = datetime.now()

class article:
    def __init__(self,info,ftext,sentiment):
        self.info = info
        self.fulltext = ftext
        self.sentiment = sentiment
#something weird with economist
for news_org in os.listdir('articles_sentiment'):
    print(news_org)
    starting_index=0

    sentiment_files = os.listdir('articles_sentiment/'  +news_org)
    fulltext_files = os.listdir('articles_fulltext/' + news_org)
    newsapi_files = os.listdir('articles_newsapi/' + news_org)

    fulltext_second_try_files = os.listdir('articles_fulltext_second_try/'+news_org)
    num_not_okay=0

  #  print (len(sentiment_files))
    for i in range(len(sentiment_files)):
  
        newsapi_fstr = 'articles_newsapi/' + news_org + '/' + newsapi_files[i]
        newsapi_file = open(newsapi_fstr,'r')
        newsapi_articles = json.load(newsapi_file)['articles']

        fulltext_fstr = 'articles_fulltext/' + news_org + '/' + fulltext_files[i]      
        fulltext_file = open(fulltext_fstr,'r')        
        fulltext_articles = json.load(fulltext_file)

        fulltext_second_try_fstr = 'articles_fulltext_second_try/' + news_org + '/' + fulltext_second_try_files[i] 
        fulltext_second_try_file = open(fulltext_second_try_fstr,'r')        
        fulltext_second_try_articles = json.load(fulltext_second_try_file)

        sentiment_fstr = 'articles_sentiment/' + news_org + '/' + sentiment_files[i]
        sentiment_file = open(sentiment_fstr,'rb')
        sentiment_articles = pickle.load(sentiment_file)
              
        print ('num articles: ' + str(len(fulltext_second_try_articles)))
        
        num_matches=0
        secondary_match=0
        bad_urls=0
        offset=-1
        z=0
        sentiment_index=0
        for article in sentiment_articles:
            
            entities = [entity.name for entity in article.entities]
            unique_entities =[]
            for entity in entities:
                if entity not in unique_entities:
                    unique_entities.append(entity)
            max_score=0
            max_index=-1
            for i in range(max_index, len(fulltext_articles)):            
                fulltext_article = newsapi_articles[i]['title']
                score = sum([1 for entity in unique_entities if entity in fulltext_article])
                if score > max_score:
                    max_score=score
                    max_index = i
            z+=1

            if z>350:
                print (article)
                print (fulltext_articles[z-1])
                print (newsapi_articles[max_index]['title'])
                print (max_score)
                print (unique_entities)
                exit()
                


            num_matches+=1
   
        exit()
                

            
              

           # print (max_score)
        exit()
      
#         with open(sentiment_fstr) as infile:
#             sentiment_results = pickle.load(infile)
            
#             for article in sentiment_results:
#                 all_article_info = []
#                 entities = [entity.name.lower() for entity in article.entities]

#                 for entity in entities:

#                     fulltext_fstr = 
#                     for fulltext_article in 
#             articles = json.load(infile)['articles']
#             print('num articles: ' + str(len(articles)))
#             i=0
#             for article in articles:
#                 print('article #' + str(i))
#                 i+=1
#                 url = article['url']             
#                 fulltext = get_fulltext(url)            
#                 # if fulltext != 'bad url': #dumb. should have appended 'bad url' instead to make things line up
#                 all_fulltext.append(fulltext)
                                                              
#         with open('articles_fulltext/' + news_org + '/' + one_day + '.json','w') as outfile:
#             json.dump(all_fulltext,outfile)
                
# print ("it has taken: " + str(datetime.now()-start))
