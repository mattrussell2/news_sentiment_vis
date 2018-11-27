import requests
import json
import sys
import math
import os
from newsapi import NewsApiClient

import argparse


#this fn checks an http status code (will print if not 200)
def check_status_code(response):
    if response.status_code != 200:
        print('whoops!')
        print('status code: ' + str(response.status_code))
        print(response.json())
        return False
    return True

def get_news_urls():

    #sources for article extraction
    sources = ['abc-news','bbc-news','breitbart-news','business-insider','buzzfeed','cbc-news','cbs-news','cnbc','cnn','financial-times','fox-news','msnbc','nbc-news','politico','the-economist','the-huffington-post','the-new-york-times','the-wall-street-journal','the-washington-post','usa-today']

    #set the date range
    dates = [str(x) for x in range(30) if x > 0 and x < 26] 

    #basic base url info for newsapi calls
    base_url = 'https://newsapi.org/v2/everything?'
    page_size = '&pageSize=100' #(100 is max size)
    api_key = '&apiKey=' + os.environ['NEWS_API_KEY'] #need bash variable saved as API key

    #iterate over all news sources
    for source in sources:
        print ("-------------------------------")
        print ("source: " + source)

        #make sure the file save path exists
        if not os.path.exists('articles_newsapi/'+source +'/'):
            os.mkdir('articles_newsapi/'+source)

        #set source string for url request
        source_str = 'sources=' + source

        #flag 
        finished_well=1
        
        #iterate over all dates
        for i in range(len(dates)):

            #specify the date
            date = dates[i]

            #skip if done this day already
            if source + '_11_' + date + '.json' in os.listdir('articles_newsapi/'+source +'/'):
                continue
           
            #time strings (just one day)
            from_str = '&from=2018-11-' + date
            to_str =   '&to=2018-11-' + date

            print ("working on date: " + date)

            #setup first newsapi call
            first_url_str = base_url + source_str + from_str + to_str + page_size + api_key            
            response = requests.get(first_url_str)

            #check to make sure call is legit
            stat_check = check_status_code(response) 
            if not stat_check: break 
        
            #setup data structure to store responses from newsapi
            one_day_articles = {'articles':[]} #kinda clunky, but works for saving to file

            #determine the number of times to call newsapi
            num_pages = math.ceil(response.json()['totalResults'] / 100)

            #flag for current set
            finished_pages = 0 
            
            #iterate over all pages 
            for i in range(1,num_pages+1):

                #call newsapi
                print ("working on page: " + str(i))
                url_str = base_url + source_str + from_str + to_str + page_size + '&page=' + str(i) + api_key
                response = requests.get(url_str)

                #check status code
                if not check_status_code(response): break

                #convert to dictionary
                response = response.json()
                articles = response['articles']

                #add article to articles
                one_day_articles['articles'].extend(articles)
                finished_pages += 1

            #if we've got all the pages in the whole day
            if finished_pages == num_pages:
             
                #save the file
                with open('articles_newsapi/'+source +'/' + source + '_11_' + date +'.json','w') as outfile:
                    json.dump(one_day_articles,outfile)
            else:            
                print ('something went wrong. did not get all pages')
                finished_well=0

        if finished_well==1:
            print ("source: " + source + " finished successfully")

    return


# #below is only for AP, which needs to be broken down by 2 calls/day b/c so many articles
# def get_news_urls_associated_press():   
#     sources = ['associated-press']

#     start_dates = [x + y for x in ['0','1','2'] for y in ['0','1','2','3','4','5','6','7','8','9']]
#     end_dates =   [x + y for x in ['0','1','2'] for y in ['0','1','2','3','4','5','6','7','8','9']]

#     start_dates.remove('00')
#     start_dates.append('30')
#     end_dates.remove('00')
#     end_dates.append('30')
        
#     start_dates = start_dates[:14] #only go until midnight on the 14th.
#     end_dates = end_dates[:14]

#     start_times = ['T00:00:00','T12:00:01']
#     end_times = ['T12:00:00','T23:59:59']
  
#     base_url = 'https://newsapi.org/v2/everything?'
#     page_size = '&pageSize=100'
#     api_key = '&apiKey=' + os.environ['NEWS_API_KEY']

#     for source in sources:
#         print ("-------------------------------")
#         print ("source: " + source)        
#         source_str = 'sources=' + source
#         finished_well=1
#         for d in range(len(start_dates)):
#             start_date = start_dates[d]
#             end_date = end_dates[d]
#             print ("working on dates: " + start_date + "-" + end_date)

#             for t in range(2):
           
#                 from_str = '&from=2018-11-' + start_date + start_times[t] #'T00:00:01'
#                 to_str =   '&to=2018-11-' + end_date + end_times[t] #'T23:59:59'
          
#                 first_url_str = base_url + source_str + from_str + to_str + page_size + api_key          
#                 response = requests.get(first_url_str)
#                 stat_check = check_status_code(response)
#                 if not stat_check: break

#                 print ("total results: " + str(response.json()['totalResults']))
#                 one_day_articles = {'articles':[]} #kinda clunky, but works for saving to file
#                 num_pages = math.ceil(response.json()['totalResults'] / 100)
#                 if num_pages > 10:
#                     too_many_pages=1
#                     print ("TOO MANY PAGES")
#                 else:
#                     too_many_pages=0
#                 finished = 0
#                 for i in range(1,num_pages+1):       
#                     print ("working on page: " + str(i))
#                     url_str = base_url + source_str + from_str + to_str + page_size + '&page=' + str(i) + api_key
#                     response = requests.get(url_str)
#                     if not check_status_code(response): break
#                     response = response.json()
#                     articles = response['articles']
#                     one_day_articles['articles'].extend(articles)
#                     finished+=1

#                 if finished==num_pages:
#                     if not os.path.exists('articles_newsapi/'+source +'/'):
#                         os.mkdir('articles_newsapi/'+source)
#                     with open('articles_newsapi/'+source +'/' + source + '_11_' + start_date + '-11_' + end_date + '_' + 'T' + str(t) + '_' + str(num_pages) +'.json','w') as outfile:
#                         json.dump(one_day_articles,outfile)
#                 else:
#                     if not too_many_pages:
#                         print ('something went wrong. did not get all pages')
#                         finished_well=0
#         if finished_well==1:
#             print ("source: " + source + " finished successfully")
#     return response


#start program here
if __name__=='__main__':
    get_news_urls()
