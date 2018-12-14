import os
import json
import sys
import pickle
import numpy as np
from scipy.stats import sem
import matplotlib.pyplot as plt
import math
import copy

long_labels = os.listdir('articles_sentiment')
short_labels = ['ABC','BBC','BBN','BI','BZFD','CBC','CBS','CNBC','CNN','FT','FOX','MSNBC','NBC','POL','ECON','HUFF','NYT','WSJ','WASH','USA']

if len(sys.argv) < 2:
    print ("please enter at least one entity")
    exit()
           
#all the entities we're interested in
entities = [entity.lower() for entity in sys.argv[1:]]

sources = ['IBM','GOOGLE','AYLIEN']
sources = sources[:-1] #skip aylien for now

#each entity for all news orgs
all_sentiment = {source: {news_org: {entity:{} for entity in entities} for news_org in long_labels} \
                 for source in sources}

#list of news orgs to remove from final listing.
to_remove=[]

#for each news org
for news_org in long_labels:        
        
    #intitialize the arrays for various important values
    for entity in entities:
        if 'AYLIEN' in sources:
            all_sentiment['AYLIEN'][news_org][entity]['polarity']=[]       
            all_sentiment['AYLIEN'][news_org][entity]['confidence']=[]
            all_sentiment['AYLIEN'][news_org][entity]['score']=[]
        if 'GOOGLE' in sources:
            all_sentiment['GOOGLE'][news_org][entity]['salience']=[]                        
            all_sentiment['GOOGLE'][news_org][entity]['magnitude']=[]
            all_sentiment['GOOGLE'][news_org][entity]['score']=[]
        if 'IBM' in sources:
            all_sentiment['IBM'][news_org][entity]['score']=[]                                            
            all_sentiment['IBM'][news_org][entity]['polarity']=[]
            all_sentiment['IBM'][news_org][entity]['relevance']=[]                
        
    #for each day
    for day in os.listdir('articles_sentiment/' + news_org):
        #  if day != os.listdir('articles_sentiment/'+news_org)[0]: continue
        #open the file
        f = open('articles_sentiment/' + news_org + '/' + day,'rb')
        articles = pickle.load(f)
        
        #for each article
        for article in articles:

            if type(article)==type('string'): continue

            #skip article if any source doesn't have a sentiment score for it
            if [1 for source in sources if source+'_sentiment' not in article.keys()]:
                continue
        
            #skip article if a sentiment score is a string (only aylien and google)
            if [source for source in sources[1:] if type(article[source + '_sentiment'])==str]:
                continue
            try:
                if 'AYLIEN' in sources: aylien_entities = article['AYLIEN_sentiment']['entities']      
                if 'GOOGLE' in sources: google_entities = article['GOOGLE_sentiment'].entities
                if 'IBM' in sources: ibm_entities = json.loads(article['IBM_sentiment'])['entities']
            except:
                continue 

            if 'AYLIEN' in sources:
                #iterate over all aylien entities for a given article
                for entity in aylien_entities:

                    #convert to lowercase
                    name = entity['mentions'][0]['text'].lower()

                    #if it's one of interest
                    if name in entities:
                        #extract relevant values
                        polarity = entity['overall_sentiment']['polarity']
                        confidence = entity['overall_sentiment']['confidence']

                        #adjust to develop 'score'                    
                        if polarity == 'negative': score = confidence * -1
                        if polarity == 'neutral':  score = 0
                        if polarity == 'positive': score = confidence

                        #save relevant values
                        all_sentiment['AYLIEN'][news_org][name]['polarity'].append(polarity)
                        all_sentiment['AYLIEN'][news_org][name]['confidence'].append(confidence)                
                        all_sentiment['AYLIEN'][news_org][name]['score'].append(score)

            if 'GOOGLE' in sources:
                # #Iterate over all google entities for a given article
                for entity in google_entities:

                    name = entity.name.lower()

                    #if it's one of interest
                    if name in entities:
                        
                        salience = entity.salience
                        magnitude = entity.sentiment.magnitude
                        score = entity.sentiment.score

                        #save relevant values
                        all_sentiment['GOOGLE'][news_org][name]['salience'].append(salience)
                        all_sentiment['GOOGLE'][news_org][name]['magnitude'].append(magnitude)
                        all_sentiment['GOOGLE'][news_org][name]['score'].append(score)

            if 'IBM' in sources:
                #iterate over all IBM entities for a given article
                for entity in ibm_entities:

                    #convert to lowercase
                    name = entity['text'].lower()                               

                    #if it's a person of interest
                    if name in entities:
                    
                        #extract relevant values
                        score = entity['sentiment']['score']
                        polarity = entity['sentiment']['label'] #positive, negative, or netural
                        relevance = entity['relevance']
                  
                        #adjust score
                        if score > 0 and polarity=='negative': score=score*-1 #make sure it's negative

                        #save relevant values
                        all_sentiment['IBM'][news_org][name]['score'].append(score)
                        all_sentiment['IBM'][news_org][name]['polarity'].append(polarity)
                        all_sentiment['IBM'][news_org][name]['relevance'].append(relevance)                                                        

    #determine if we need to remove this news org
    remove_it = False
    for source in sources:
        if [1 for entity in entities if all_sentiment[source][news_org][entity]['score']==[]]:    
            remove_it = True
            break

    #remove the news org from all sources
    if remove_it:
        for source in sources:
            del all_sentiment[source][news_org]
        to_remove.append(news_org)        

# remove any news orgs that don't have any sentiment values for any entity of interest
for org in to_remove: 
    short_labels.pop(long_labels.index(org))
    long_labels.remove(org)   


stats = ['means','medians','serrs']

#structure: {'IBM': 'means': {'e1': [],'e2':[]}, 'medians': {'e1':[],'e2':[]},'GOOG'}, etc.
all_stats = {source:{stat:{x:[] for x in entities} for stat in stats} for source in sources}

#print(all_stats)
#exit()
    
#for IBM, GOOG, and AYLIEN
for source in sources:

    #for all entities provided by user
    for entity in entities:
        
        #for all news sources
        for i in range(len(long_labels)):

            #nab corresponding news source
            news_org = long_labels[i]     

            #extract mean, median, and serr from that news source toward that entity, and add it to all_stats
            all_stats[source]['means'][entity].append(np.mean(all_sentiment[source][news_org][entity]['score']))
            all_stats[source]['medians'][entity].append(np.median(all_sentiment[source][news_org][entity]['score']))
            all_stats[source]['serrs'][entity].append(sem(all_sentiment[source][news_org][entity]['score']))            
            
print (all_stats)

#width of bar reflecting sentiment for given news source toward various entities
width=0.5

#do some magic to allow even/odd number of entities entered by user, but still maintain balance when graphing
#not going to comment in depth here...suffice it to say, it will display bars evenly around each axis point,
#with an even or odd number of entities per news source
if len(entities)==1:
    offsets = [0]
else:
    pre_post_size = math.floor(len(entities)/2.0)   
    offsets = [width*x/len(entities) for x in range(-pre_post_size,pre_post_size+1)]
    
    if len(entities) % 2 == 0:
        offsets.remove(0.0)
        for i in range(len(offsets)):
            offset = offsets[i]
            if offset < 0:                
                offset = offset + width/len(entities)/2.0
            else:
                offset = offset - width/len(entities)/2.0
            offsets[i] = offset

#more than one color for more than one entity
colors = ['Red','Blue','Green','Yellow','Orange','Pink']

#one graph per analysis source (IBM< google, aylien)
for source in sources:
    #index
    ind = np.arange(len(long_labels))
    fig, ax = plt.subplots()

    #all_stats[source]['means'][entity] contains a list
    #    of values, which are ordered by news org
    for i in range(len(entities)):
        ax.bar(offsets[i]+ind,
               all_stats[source]['means'][entities[i]],
               width/len(entities),
               yerr=all_stats[source]['serrs'][entities[i]],
               color=colors[i],label=entities[i])

        ax.set_xticks(ind)
        ax.set_xticklabels(short_labels)
        ax.set_yticks(np.arange(-1,1,.1))
        ax.legend()
        
        plt.title('entity sentiment data as analyzed by: ' + source)
        plt.show()
