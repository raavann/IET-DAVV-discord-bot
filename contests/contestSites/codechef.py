from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime

import contests.data_class as data_class
import db.contest_data as contest_data

def get_codechef_contests():
    codechef_url = 'https://www.codechef.com/contests'

    chrome_options = Options()
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
        
    codechef_browser = webdriver.Chrome(options=chrome_options)
    codechef_browser.get(codechef_url)

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

    codechef_browser.quit()
