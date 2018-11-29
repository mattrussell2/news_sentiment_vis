import os
import json
from aylienapiclient import textapi
from aylienapiclient.errors import HttpError
AYLIEN_service = textapi.Client(os.environ['AYLIEN_APP_ID'],os.environ['AYLIEN_KEY'])

            
for news_org in os.listdir('articles_fulltext/'):
    if news_org !=  'the-washington-post': continue
    for f in os.listdir('articles_fulltext/'+news_org):
        if '16' not in f: continue
        fstr = 'articles_fulltext/' + news_org + '/' + f
        orig = open(fstr)
        json = json.load(orig)
        #        print (json[7])
     #   print(json[179]['url'])
        print (json[138]['fulltext']=="")
        try:
            aylien_result = AYLIEN_service.Elsa({'text':json[9]['fulltext']})
        except HttpError as e:
            print('403' in str(e))
         #   print(aylien_result)

        #print(aylien_result)
        rate_limits = AYLIEN_service.RateLimits()
        print(rate_limits)
        # if (rate_limits['remaining']==1):
        #     print("reached daily Aylien rate limit")
        #     break
        # print (len(json))
        exit()
