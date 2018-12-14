from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from watson_developer_cloud import WatsonApiException

from google.cloud import language
from google.cloud.language import enums,types
from google.api_core.exceptions import InvalidArgument,InternalServerError

from aylienapiclient import textapi
from aylienapiclient.errors import HttpError

import time
import os
import pickle
import copy
import json

#this script iterates over all the saved fulltext articles, queries the IBM, GOOGLE, and AYLIEN apis, and
#adds the sentiment analysis info to each article

#set up the IBM natural language API
#$IBM_CREDS must be a defined as bash var
IBM_service = NaturalLanguageUnderstandingV1(
     version = '2018-03-19',
     url = 'https://gateway-wdc.watsonplatform.net/natural-language-understanding/api',
     iam_apikey = os.environ["IBM_CREDS"])

#set up Google natural language API
#$GOOGLE_APPLICATION_CREDENTIALS has to be defined as bash var
GOOGLE_service = language.LanguageServiceClient()

#set up AYLIEN text api
#$AYLIEN_APP_ID and $AYLIEN_KEY must be defined as bash vars
AYLIEN_service = textapi.Client(os.environ['AYLIEN_APP_ID'],os.environ['AYLIEN_KEY'])
aylien_timer=0 #can only make a certain # of calls per minute. 

sources = ['IBM','GOOGLE']#,'AYLIEN']

#iterate over all news orgs that have fulltext files
for news_org in os.listdir('articles_fulltext'):
    print (news_org)

    #make sure file save path exists
    if not os.path.exists('articles_sentiment/' + news_org):
        os.mkdir('articles_sentiment/' + news_org)

    #for each day for the news org
    for one_day in os.listdir('articles_fulltext/'+news_org)[8:]: #skip first day(already done)      
        print('starting day ' + one_day)
        
        #load the fulltext article
        fstr = 'articles_fulltext/' + news_org + '/' + one_day
        f = open(fstr)
        one_day_articles = json.load(f)

        #if the file already exists
        if one_day in os.listdir('articles_sentiment/' + news_org):

            #open it
            f = open('articles_sentiment/' + news_org + '/' + one_day,'rb')
            one_day_articles = pickle.load(f)

            #iterate over the article objects
            for i in range(len(one_day_articles)):
                #if we don't find any of the analysis sources for a given article, start at that location
                if [1 for source in sources if source+'_sentiment' not in one_day_articles[i].keys()]:
                    start_loc = i
                    break      

        #otherwise, just set starting article as the first one
        else:
            start_loc = 0
         
        #for each article for that day
        #ONLY 10 articles at a time, for now
        #min(start_loc+10,len(one_day_articles))):
        for i in range(start_loc,len(one_day_articles)): 
          #  if i > len(one_day_articles)-1: continue
            print("starting article #{}".format(i))
          
            #extract the fulltext
            ftext = one_day_articles[i]['fulltext']
            if ftext=="":
                print("skipping article b/c empty")
                continue #skip empty text articles

            if ftext=="bad url":
                print("skipping article b/c bad url")
                continue
            if 'IBM' in sources:
            #only get IBM sentiment for this article if it's not there already            
                if 'IBM_sentiment' not in one_day_articles[i].keys():
                    
                    #analyze the text via IBM
                    try:
                        ibm_response = IBM_service.analyze(text = ftext,
                                                           features = Features(entities=EntitiesOptions(sentiment=True))).get_result()
                        ibm_response = json.dumps(ibm_response,indent=2)                
                    except WatsonApiException as e:                    
                        print (e.message)
                        print (ftext)                   
                        if 439 == int(e.code):
                            break #too many requests                                                
                        ibm_response = "IBM sentiment analysis failed with message: " + e.message

                    #save the IBM response inside the original article object
                    one_day_articles[i]['IBM_sentiment'] = ibm_response

            if 'GOOGLE' in sources:
                #only get Google sentiment for this article if it's not there already
                if 'GOOGLE_sentiment' not in one_day_articles[i].keys():
                
                    #analyze the text via Google
                    try:
                        document = types.Document(
                            content = ftext,
                            type = enums.Document.Type.PLAIN_TEXT)
                        google_response = GOOGLE_service.analyze_entity_sentiment(document=document)
                    except InvalidArgument as e:
                        print ('language error')
                        google_response = 'language error in sentiment extraction'
                    except InternalServerError as e:
                        print ('server error UTF issue')
                        google_response = 'server error - binary in fulltext file'
                    except:
                        print("other google error")
                        break #don't add to file
                    
                #save the Google response inside the original article object
                one_day_articles[i]['GOOGLE_sentiment'] = google_response

            if 'AYLIEN' in sources:
                #only get Aylien for this article if it's not there already
                if 'AYLIEN_sentiment' not in one_day_articles[i].keys():

                    #make sure not to breach the 60 calls per minute rule (actual number is lower)
                    if(aylien_timer>=20): #getting errors with higher numbers...sleep more often
                        print("need to rest to make Aylien happy")
                        time.sleep(90)    #should only be 60, but getting errors, so let's be safe
                        aylien_timer=0

                        #analyze via AYLIEN
                    try:
                        aylien_result = AYLIEN_service.Elsa({'text':ftext})
                        aylien_timer+=1

                        #handle exceptions gracefully
                    except HttpError as e:                
                        print(e)
                        break #don't add to file
                        
                    #save the AYLIEN response inside the original article object
                    one_day_articles[i]['AYLIEN_sentiment'] = aylien_result              

                    #check the remaining daily rate limit
                    rate_limits = AYLIEN_service.RateLimits()
                    if (rate_limits['remaining']==1):
                        print("reached daily Aylien rate limit")
                        exit()
                
        #save the file
        with open('articles_sentiment/' + news_org + '/' + one_day,'wb') as outfile:            
            pickle.dump(one_day_articles,outfile)
            print('pickled')
    
        break #for now, just do the first day
