from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time


def get_user_info(user_link):
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(user_link)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
    	lastCount = lenOfPage
    	time.sleep(3)
    	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;  return lenOfPage;")
    	if lastCount==lenOfPage:
    		match=True


    html = driver.page_source

    soup = BeautifulSoup(driver.page_source, "lxml")

    ques_text= soup.find_all('span', {'class': 'TopicNameSpan'})
    words = []
    for i in range(0,len(ques_text)):
        words.append(ques_text[i].get_text())

    return words
