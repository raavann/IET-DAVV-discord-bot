from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from datetime import datetime,timedelta

import contests.data_class as data_class
import db.contest_data as contest_data

def create_browser():
    global codeforces_url
    codeforces_url = 'https://codeforces.com/contests'

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
  
    global codeforces_browser
    codeforces_browser = webdriver.Chrome(options=chrome_options)
    codeforces_browser.get(codeforces_url)

def get_upcoming_contests():
    codeforces_browser.refresh()
    html = codeforces_browser.page_source
    codeforces_page = BeautifulSoup(html,'lxml')

    table_html = codeforces_page.find('div',class_ = 'datatable')
    table_rows = table_html.find_all('tr')
    table_rows.pop(0)
    for tr in table_rows:
        td = tr.find_all('td')  
        name,b,stime,len_co,e,f=td
        del b,e,f
        time_ = len_co.text.strip()
        if(len(time_) > 5):
            t = datetime.strptime(time_,"%d:%H:%M")
            len_co = timedelta(days=t.day,hours=t.hour, minutes=t.minute)
        else:
            t = datetime.strptime(time_,"%H:%M")
            len_co= timedelta(hours=t.hour, minutes=t.minute)
        
        st = datetime.strptime(stime.text.strip(),"%b/%d/%Y %H:%MUTC+5.5")
        Id = tr['data-contestid']
        contest = data_class.Contest(
            Id,
            codeforces_url+'/'+Id,
            name.text.strip(),
            st,
            st+len_co,
        )

        #insert into database, exception handling already done
        contest_data.insert_cont(contest)

