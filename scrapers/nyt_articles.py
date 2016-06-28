import json
from bs4 import BeautifulSoup
import feedparser
import urllib2
import re
from time import sleep
import requests
from datetime import datetime, timedelta
from cookielib import CookieJar

def get_stories():
    urls = []
    file_path = '../data/urls/nyt_urls'
    with open(file_path,'r') as f:
        for line in f:
            if ("/2016" in line) and ("/sports/" not in line):
                urls.append(line.strip('\n'))

    for story_url in urls[10:]:
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        p = opener.open(story_url)
        story = p.read()
        soup = BeautifulSoup(story,'html.parser')
        story_file_name = ''
        story_text_all = ''
        try:
            story_title = soup.find_all('title', {'class': ''})[0].string.strip()
            story_title = story_title.rstrip(' - The New York Times')
            story_date = soup.find_all('meta',{'name':'pdate'})[0].attrs['content']
            story_body = soup.find_all("p", { "class" : "story-body-text story-content" })
            story_text = []
            for snippet in story_body:
                html = str(snippet)
                soup_s = BeautifulSoup(html,'html.parser')
                story_text.append(soup_s.getText().encode("UTF-8"))
            story_text_all = ''.join(story_text)
            story_file_name = story_url[story_url.rfind('/')+1:-5]
        except:
            print 'bad url. could not get story'

        if len(story_file_name)>0 and len(story_text_all)>0:
            file_url = '../data/nyt/'+ story_file_name
            file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
            with open(file_url,'w') as f:
                f.write(json.dumps(file_content))
        sleep(4)

if __name__ == '__main__':
    #file_path = sys.argv[1]
    print 'getting stories'
    get_stories()
    print 'done!'
