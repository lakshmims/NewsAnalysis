import json
import re
from time import sleep
import requests
from datetime import datetime, timedelta
import os
from cookielib import CookieJar


def get_story_urls():
    api_key = os.environ['NYT_API_KEY']
    story_urls = []
    story_docs = []

    #format today's date
    new_date = datetime.now()
    day = "0"+str(new_date.day)
    month = "0"+str(new_date.month)
    year = str(new_date.year)
    end_date = year+month[-2:]+day[-2:]

    #end_date = "20160620"

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    facet_field = "section_name"

    # for dt in xrange(50):
    #     end_date = get_previous_date(end_date)
    story_docs = []
    story_urls = []
    for page in xrange(1,3):
        #params = {"api-key":api_key,"facet_field" : facet_field, "end_date": end_date, "sort": "newest" , "page": str(page)}
        params = {"api-key":api_key, "sort": "newest" , "page": str(page)}
        response = requests.get(url,params=params)
        content = json.loads(response.content)
        if content['status'] == 'OK':
            story_docs.append(content['response']['docs'])
            last_story_date = story_docs[-1][-1]['pub_date']

            story_urls = [row['web_url'] for doc in story_docs for row in doc]
            print story_urls

            with open('../data/urls/nyt_urls','a') as f:
                for row in story_urls:
                    f.write(row.encode('utf8')+'\n')

            # if date_diff(last_story_date, end_date):
            #     break
        else:
            print 'Status NOT OK'

        sleep(3)

def date_diff(last_story_date, query_date):
    dt = re.sub('-', '', last_story_date[0:10])
    if dt !=query_date:
        return True
    else:
        return False

def get_previous_date(end_date):
    previous_date = datetime.strptime(end_date, '%Y%m%d')
    d = timedelta(days=1)
    return datetime.strftime(previous_date-d, '%Y%m%d')

if __name__ == '__main__':
    #file_path = sys.argv[1]
    print 'getting urls'
    get_story_urls()
    print 'done!'
