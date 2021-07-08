from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from datetime import datetime,timedelta

import contests.data_class as data_class

def create_browser():
    codechef_url = 'https://www.codechef.com/contests'

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    global codechef_browser 
    codechef_browser = webdriver.Chrome(options=chrome_options)
    codechef_browser.get(codechef_url)

#get data of contest that started, but has not ended yet.
def get_present_contests(dict_x,time_list):
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
            dict_x[contest.id] = [contest]
            time_list.append(data_class.Time_List(contest.start_time,'s',contest.id))
            time_list.append(data_class.Time_List(contest.end_time,'e',contest.id))


def get_upcoming_contests(dict_x,time_list):
################################ past contest for testing ###################################3
    codechef_browser.refresh()
    html = codechef_browser.page_source
    codechef_page = BeautifulSoup(html,'lxml')

    table_html = codechef_page.find(id = 'past-contests-data')
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

        #only add in dictionary dict_x if the 'code' is not already present
        if contest.id not in dict_x:
            dict_x[contest.id] = [contest]
            time_list.append(data_class.Time_List(contest.start_time,'s',contest.id))
            time_list.append(data_class.Time_List(contest.end_time,'e',contest.id))
