import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import re
import requests
from selenium.webdriver.chrome.options import Options
import time
import datetime as dt
from os import listdir
from bs4 import BeautifulSoup

def crawl_stock_transcript(ticker,try_times):
    url = 'https://seekingalpha.com/article/4514532-nvidia-corporation-nvda-ceo-jensen-huang-on-q1-2023-results-earnings-call-transcript'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    false = False
    null = None
    true = True
    tt = eval(soup.find_all('script')[15].text[18:-1])
    content_word = tt['article']['response']['data']['attributes']['content']
    savingdict = {}
    savingdict['content'] = content_word
    ticker = 'NVDA'
    y = 2022
    m = 2
    d = 16
    with open(f'{ticker}_{y}_{m}_{d}.json', 'w') as z:
        json.dump(savingdict,z)

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(r'C:\Users\Bray\AppData\Local\Programs\Python\Python39\Lib\site-packages\webdriver_manager\chromedriver',options=chrome_options)
ticker='nvda'
crawl_stock_transcript(ticker,0)