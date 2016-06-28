import json
from bs4 import BeautifulSoup
import re
from time import sleep
import requests
from cookielib import CookieJar
from selenium import webdriver
from unidecode import unidecode
import os
import sys


def wsj_login(username,password):
    # username = os.environ['WSJ_USER_ID']
    # password = os.environ['WSJ_PASSWORD']
    url = 'https://id.wsj.com/access/pages/wsj/us/signin.html?url=http%3A%2F%2Fwww.wsj.com&mg=id-wsj'
    driver = webdriver.Firefox()
    driver.get(url)

    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(username)

    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(password)

    driver.find_element_by_id('submitButton').click()
    sleep(10)
    return driver

def get_story_urls(driver):
    article_pages = []
    for page in xrange(1,100):
        url = 'http://www.wsj.com/search/term.html?KEYWORDS=a&isAdvanced=true&daysback=90d&andor=AND&sort=date-desc&source=wsjarticle'
        url = url+'&page='+str(page)
        #driver = webdriver.Firefox()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        x = soup.find_all(re.compile('a.*\:a'),{"class":""})
        y = [item['href'] for item in x]
        z = ["www.wsj.com"+(link) for link in y if "/articles/" in link]
        article_pages.extend(z)
        with open('../data/urls/wsj_urls','a') as f:
            for row in z:
                f.write(row.encode('utf8')+'\n')
        sleep(8)

if __name__ == '__main__':
    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    driver = wsj_login(username,password)
    print 'login successful'
    print 'getting urls'
    get_story_urls(driver)
    print 'done!'
