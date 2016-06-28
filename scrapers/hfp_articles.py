import json
from bs4 import BeautifulSoup
import urllib2
#import re
from time import sleep
import requests
import sys

#import requests
#from datetime import datetime, timedelta
#from cookielib import CookieJar

def get_stories(file_path):
    urls = []
    file_path = '../data/urls/hfp_urls'
    with open(file_path,'r') as f:
        for line in f:
            urls.append(line.strip('\n'))
    # cj = CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    for story_url in urls[0:10]:

        story_file_name = ''
        story_text_all = ''
        try:
            response = requests.get(story_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            story_text_all = soup.find_all("div", { "class" : "content-list-component text" })[0].text
            story_file_name = story_url[story_url.rfind('/')+1:story_url.rfind('.html')]
            story_title = soup.find_all('title', {'class': ''})[0].string.strip()
            story_date = soup.find_all('span',{'class':'timestamp__date--published'})[0].text
            story_date = story_date[0:10].replace('/','')
        except:
            print 'could not get story', story_url

        if len(story_file_name)>0 and len(story_text_all)>0:
            file_url = '../data/articles/hfp/'+ story_file_name
            file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
            with open(file_url,'w') as f:
                f.write(json.dumps(file_content))
        sleep(1)




if __name__ == '__main__':
    print 'getting stories'
    file_path = sys.argv[1]
    get_stories(file_path)
    print 'done!'
