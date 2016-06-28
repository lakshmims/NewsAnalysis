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


def get_stories(file_path, driver):
    urls = []
    with open(file_path,'r') as f:
        for line in f:
            urls.append(line.strip('\n'))
    for story_url in urls:
        driver.get(story_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        story_date = soup.find('meta', attrs={'itemprop': 'datePublished'}).attrs['content'][0:10].replace('-','')
        story_title = soup.find('h1', attrs={'class': 'wsj-article-headline', 'itemprop': 'headline'}).text
        story_file_name = story_url[story_url.rfind('/')+1:]
        story_body = soup.find('div', attrs={'id': 'wsj-article-wrap', 'itemprop': 'articleBody'})
        story_text = story_body.findAll('p')
        story_text_all = unidecode(' '.join([line.text for line in story_text]))
        if len(story_file_name)>0:
            file_url = '../data/wsj/'+ story_file_name
            file_content = { 'url':story_url, 'title':story_title, 'date':story_date, 'content':story_text_all}
            with open(file_url,'w') as f:
                f.write(json.dumps(file_content).encode("UTF-8"))
        sleep(2)

if __name__ == '__main__':
    file_path = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    driver = wsj_login(username,password)
    print 'login successful'
    print 'getting stories'
    get_stories(file_path,driver)
    print 'done!'
