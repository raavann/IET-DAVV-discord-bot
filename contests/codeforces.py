import json
from datetime import datetime,timedelta
from contests.data_class import Contest
from urllib.request import urlopen
from db.contest_data import insert_cont

def get_upcoming_contests():
    url = "https://codeforces.com/api/contest.list"
    response = urlopen(url)
    data_json = json.loads(response.read())

    for item in data_json['result']:
        if(item['phase'] == "FINISHED"):
            break
        lenco = timedelta( seconds =item['durationSeconds'])
        st = datetime.fromtimestamp(item['startTimeSeconds'])
        et = st+lenco
        x = str(item['id'])
        link = "".join(['https://codeforces.com/contests/',x])
        cont = Contest(item['id'],link,item['name'] ,st,et)
        
        insert_cont(cont)
