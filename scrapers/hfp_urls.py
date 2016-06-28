import json
import re
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep
import requests

now = datetime.now()
dayless = timedelta(days=1)
new_date = now-dayless
new_date.day

#def get_story_urls():
story_urls = []
story_docs = []
urls = []
new_date = datetime.now()
​
for i in xrange(200):
            day = new_date.day
            month = new_date.month
            url = "http://www.huffingtonpost.com/archive/2016-{}-{}".format( month , day)
            urls.append(url)
            dayless = timedelta(days=i)
            new_date = now-dayless
article_urls = []
for url in urls[0:100]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.find_all('a',{ "class" : "" })
    y = [link["href"] for link in x if "/2016/" in link["href"] ]
    print y
    article_urls.extend(y)
    sleep(1)
article_urls_filtered = [url for url in article_urls if url.find('ir=Entertainment')==-1 and url.find('ir=Green')==-1]
with open('../data/urls/hfp','w') as f:
    for row in article_urls_filtered:
        f.write(row.encode('utf8')+'\n')



​
