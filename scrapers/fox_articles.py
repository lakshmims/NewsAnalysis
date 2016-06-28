import json
from bs4 import BeautifulSoup
import urllib2
from time import sleep
from cookielib import CookieJar
from selenium import webdriver
from unidecode import unidecode
from sys import argv

def get_stories(file_path):
    urls = []
    #file_path = 'data/fox_urls'
    with open(file_path,'r') as f:
        for line in f:
            urls.append(line.strip('\n'))
    for story_url in urls:
        #print story_url
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        p = opener.open(story_url)
        story = p.read()
        soup = BeautifulSoup(story,'html.parser')
        story_file_name = story_url[story_url.rfind('/')+1:-5]
        story_title = soup.find_all('title', {'class': ''})[0].string.strip()
        story_title = story_title.rstrip(' | Fox News')
        story_date = soup.find_all('meta',{'name':'dc.date'})[0].attrs['content']
        story_body = soup.find_all("div", { "class" : "article-text" })
        story_text = []
        story_text_all = ''
        for snippet in story_body:
            html = str(snippet)
            soup_s = BeautifulSoup(html)
            story_text.append(unidecode(soup_s.getText()))

        story_text_all = '\n'.join(story_text)

        if len(story_file_name)>0:
            file_url = '../data/fox/'+ story_file_name

            file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
            with open(file_url,'w') as f:
                f.write(json.dumps(file_content).encode("UTF-8"))
        sleep(5)


if __name__ == '__main__':
    print 'getting stories'
    file_path = argv[1]
    get_stories(file_path)
    print 'done!'
