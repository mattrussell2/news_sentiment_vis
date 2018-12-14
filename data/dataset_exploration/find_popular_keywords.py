from scipy.stats import sem
import matplotlib.pyplot as plt
import math
import os
import pickle
import numpy as np

long_labels = os.listdir('articles_sentiment')
short_labels = ['ABC','AP','BBC','BLOOM','BBN','BI','BZFD','CBC','CBS','CNBC','CNN','FT','FOX','MSNBC','NBC','POL','ECON','HUFF','NYT','WSJ','WASH','USA']

sources = ['IBM','GOOGLE','AYLIEN']
all_sentiment = {source: {news_org:{} for news_org in long_labels} for source in sources}
to_remove=[]

#for each news org
for news_org in long_labels:        

    #for each day
    for day in os.listdir('articles_sentiment/' + news_org):

        #open the file
        f = open('articles_sentiment/' + news_org + '/' + day,'rb')
        articles = pickle.load(f)

        #for each earticle
        for article in articles:                           
            #skip poorly formatted articles
            if type(article)==type('string'): continue

            if 'GOOGLE' in sources:            
                #for each entity listed in the article
                if 'GOOGLE_sentiment' not in article.keys(): continue
                article = article['GOOGLE_sentiment']
                if type(article)==str: continue
                for entity in article.entities:
                    if float(entity.sentiment.magnitude) * float(entity.sentiment.score) > .85 or \
                       float(entity.sentiment.magnitude) * float(entity.sentiment.score) < -.85:
                        entity.name = entity.name.lower()
                        if entity.name not in all_sentiment['GOOGLE'][news_org]:
                            all_sentiment['GOOGLE'][news_org][entity.name]=1
                        else:
                            all_sentiment['GOOGLE'][news_org][entity.name]+=1

                        
#interesting keywords:
#president (~-.1)
#state (~-.5)
#cnn - nbc's value is ~-.7 with little std error
#government
#shooting
#twitter - 0.6 positive for MSNBC
#Trump (&Obama)
#football, soccer, baseball (ABC -.7 on soccer)
#migrants (nothing)

#after these, adjusted values to only take on those with high magnitude.
#police - generaly negative.
#trump & obama. BOTH negative. Breitbart was more negative on trump than on obama

#apple, amazon, google - apple has some of most positive ratings
#WHAT THE FUCK ARE PEOPLE HAPPY ABOUT? lmfao.
#through trial and error, found some positives:
# JOBS. innovation. insight. perspective

#words associated with most passion in news organizations?


#these are obviously not what we want, or i've already checked them out
#blacklist = ['People','Ap','Browser','Company','Countries','Country', 'Image copyright','Image Caption','More','One','President','Caption','Cookies','Way','Loading','State','Government','Newsletter','Javascript','Transcript','Points','Image caption','Report','Game','Trump','donald trump','job','innovation','team','thing','some','support','things']

blacklist = ['people','thing','media playback']

blacklist = [x.lower() for x in blacklist] #they're actually all lowercase
#for each news org
total_max_seen=0#,0,0,0,0,0,0,0,0,0]
total_max_entities=''#,'','','','','','','','','']
for news_org in long_labels:        
    org_max_seen=0#,0,0,0,0,0,0,0,0,0]
    org_max_entity=''#,'','','','','','','','','']
    for entity in all_sentiment['GOOGLE'][news_org]:
        if entity in blacklist: continue       
        if all_sentiment['GOOGLE'][news_org][entity] > org_max_seen:
            org_max_seen=all_sentiment['GOOGLE'][news_org][entity]
            org_max_entity=entity
        if org_max_seen > total_max_seen:
            total_max_seen=org_max_seen
            total_max_entities=entity
    print ('news org: ' + news_org)
    print (str(org_max_seen))
    print (org_max_entity)

print ("TOTALS")
print (str(total_max_seen))
print (total_max_entities)
                         
# #means[entity] is a list of means - one per news source
# all_stats = {'means':{}, 'medians':{},'serrs':{}}
# for stat in all_stats:
#     all_stats[stat] = {entity:[] for entity in entities}
    
# for i in range(len(long_labels)):
#     news_org = long_labels[i]
#     for entity in entities:
#         all_stats['means'][entity].append(np.mean(all_sentiment[news_org][entity]))
#         all_stats['medians'][entity].append(np.median(all_sentiment[news_org][entity]))
#         all_stats['serrs'][entity].append(sem(all_sentiment[news_org][entity]))

        
# ind = np.arange(len(long_labels))
# fig, ax = plt.subplots()
# width=0.5


# if len(entities)==1:
#     offsets = [0]
# else:
#     pre_post_size = math.floor(len(entities)/2.0)
#     print(pre_post_size)

#     offsets = [width*x/len(entities) for x in range(-pre_post_size,pre_post_size+1)]
#     print (offsets)
    
#     if len(entities) % 2 == 0:
#         offsets.remove(0.0)
#         for i in range(len(offsets)):
#             offset = offsets[i]
#             if offset < 0:                
#                 offset = offset + width/len(entities)/2.0
#             else:
#                 offset = offset - width/len(entities)/2.0
#             offsets[i] = offset
      
# print(offsets)
# colors = ['Red','Blue','Green','Yellow','Orange','Pink']

# for i in range(len(entities)):
#     ax.bar(offsets[i]+ind,
#            all_stats['means'][entities[i]],
#            width/len(entities),
#            yerr=all_stats['serrs'][entities[i]],
#            color=colors[i],label=entities[i])

# ax.set_xticks(ind)
# ax.set_xticklabels(short_labels)
# ax.set_yticks(np.arange(-1,1,.1))
# ax.legend()


# plt.show()
