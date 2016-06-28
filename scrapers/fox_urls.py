import json
from bs4 import BeautifulSoup
import feedparser
import urllib2
import re
from time import sleep
import requests
from cookielib import CookieJar
import selenium
from selenium import webdriver


def get_story_urls(driver):
    article_pages = []
    for page in xrange(0,1000,10):
        url = 'http://www.foxnews.com/search-results/search?q=a&ss=fn&sort=latest&section.path=fnc/politics,fnc/us,fnc/world&start='
        url = url+str(page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_pages.extend(soup.find_all('a',{'class':'ng-binding', 'ng-bind':'article.title'}))
        sleep(5)

    with open('../data/urls/fox_urls','w') as f:
        for row in article_pages:
            f.write(row['href'].encode('utf8')+'\n')


if __name__ == '__main__':

    print 'getting urls'
    driver = webdriver.Firefox()
    get_story_urls(driver)
    print 'done!'
