import os
import pickle
import json

#each file represents one day in one news org
#file is structured as an array of dictionaries
#dictionaries have keys:
#-----------------------
#(all below are from the call to newsapi)
#source - abc, cnn, etc
#author - name(s) of author(s)
#title - title of article
#description - brief description of article
#url - url of article
#urlToImage - honestly not sure
#publishedAt - date & time of publication
#content - slightly longer version of article text
#--------------------
#fulltext - the fulltext object from the call to newspaper3k
#------------------------
#IBM_sentiment - the result of a call to IBM language API
#GOOGLE_sentiment - the result of a call to GOOGLE language API
#AYLIEN_sentiment - the result of a call to AYLIEN textapi API
#------------------------
#the example below shows how to nab the various bits of info from the
#google and IBM objects

for news_org in os.listdir('articles_sentiment'):
    print(news_org)
    for one_day in os.listdir('articles_sentiment/'+news_org):
        print(one_day)

        #open the file
        fstr = 'articles_sentiment/' + news_org + '/' + one_day
        f = open(fstr,'rb')
        one_day_articles = pickle.load(f)

        #iterate over all articles in the given day for the given news org
        for article in one_day_articles:
            if 'IBM_sentiment' in article.keys() and \
               'GOOGLE_sentiment' in article.keys() and \
               'AYLIEN_sentiment' in article.keys():

                try:
                    for entity in article['GOOGLE_sentiment'].entities:
                        #print (entity)
                        print ('source: {}'.format(article['source']))
                        print ('name: ' + entity.name)
                        print ('salience: {}'.format(entity.salience))
                        print ('magnitude: {}'.format(entity.sentiment.magnitude))
                        print ('score: {}'.format(entity.sentiment.score))
                        if "wikipedia_url" in entity.metadata.keys():
                            print ('wikipedia_url: {}'.format(entity.metadata['wikipedia_url']))

                        # for entity in json.loads(article['IBM_sentiment'])['entities']:

                        # print (entity)
                        #  print('name: ' + entity['text'])
                        #  print('score: {}'.format(entity['sentiment']['score']))
                        #  print('label: ' + entity['sentiment']['label']) #positive, negative, or netural
                        #  print('relevance: {}'.format(entity['relevance']))
                        #  print('count: {}'.format(entity['count']))
                        print( article.keys())

                        # if 'ALYIEN_sentiment' in article.keys():

                    #for entity in article['AYLIEN_sentiment']['entities']:
                    #    print(entity)
                        # print('name: ' + entity['mentions'][0]['text'])
                        # print('polarity: ' + entity['overall_sentiment']['polarity'])
                        # print('confidence: {}'.format(entity['overall_sentiment']['confidence']))

                #entity was bad for some reason
                #i.e. call to google/aylien/ibm returned an error
                #so ignore this article
                except:
                    continue
