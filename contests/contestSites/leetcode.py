from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime

from contests.data_class import Contest
from db.contest_data import insert_cont
import asyncio

async def get_leetcode_contests():
    leetcode_url = 'https://www.leetcode.com/contest/'

    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    
    leetcode_browser = webdriver.Chrome(options=chrome_options)
    leetcode_browser.get(leetcode_url)
    await asyncio.sleep(5)

    html = leetcode_browser.page_source
    leetcode_page = BeautifulSoup(html,'lxml')

    primary = leetcode_page.find(class_ = 'contest-card contest-panel primary-contest')
    biweekly = leetcode_page.find(class_ = 'contest-card contest-panel biweekly-contest')
    conts = [primary,biweekly]

    for cont in conts:
        name = cont.find(class_='card-title false').text
        code_a = name.split(" ")
        code = code_a[0]+code_a[2]
        link = 'https://www.leetcode.com'+cont.a['href']
        ar =cont.find(class_ = 'time').text
        start = datetime.strptime(ar[0:12]+"0"+ar[15:22], "%b %d, %Y%I:%M %p")
        end = datetime.strptime(ar[0:12]+"0"+ar[25:32], "%b %d, %Y%I:%M %p")

        insert_cont(Contest(code,link,name,start,end))
    
    leetcode_browser.quit()
