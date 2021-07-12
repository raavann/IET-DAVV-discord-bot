from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from datetime import datetime,timedelta

import contests.data_class as data_class
import db.contest_data as contest_data

def create_browser():
    codechef_url = 'https://www.codechef.com/contests'

    chrome_options = Options()
    #15 for heroku
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    
    global codechef_browser 
    codechef_browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    codechef_browser.get(codechef_url)

#get data of contest that started, but has not ended yet.
def get_present_contests():
    codechef_browser.refresh()
    html = codechef_browser.page_source
    codechef_page = BeautifulSoup(html,'lxml')

    table_html = codechef_page.find(id = 'present-contests-data')
    table_rows = table_html.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')  
        contest_id, name, start_time, end_time = td
        contest = data_class.Contest(
            contest_id.text,
            'https://www.codechef.com' + name.a['href'],
            name.text,
            datetime.strptime(start_time.text, "%d %b %Y  %H:%M:%S"),
            datetime.strptime(end_time.text, "%d %b %Y  %H:%M:%S"),
        ) 
        #only upto long challenges(10)
        if contest.end_time <= (datetime.now()+timedelta(days=10)):
            contest_data.insert_cont(contest)


def get_upcoming_contests():
    codechef_browser.refresh()
    html = codechef_browser.page_source
    codechef_page = BeautifulSoup(html,'lxml')

    table_html = codechef_page.find(id = 'future-contests-data')
    table_rows = table_html.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')  
        contest_id, name, start_time_str, end_time_str = td
        contest = data_class.Contest(
            contest_id.text,
            'https://www.codechef.com' + name.a['href'],
            name.text,
            datetime.strptime(start_time_str.text, "%d %b %Y  %H:%M:%S"),
            datetime.strptime(end_time_str.text, "%d %b %Y  %H:%M:%S"),
        )

        #insert into database, exception handling already done
        contest_data.insert_cont(contest)
