import json
from datetime import datetime,timedelta
from contests.data_class import Contest
from urllib.request import urlopen
from db.contest_data import insert_cont

def get_codeforces_contests():
    url = "https://codeforces.com/api/contest.list"
    response = urlopen(url)
    data_json = json.loads(response.read())

    for item in data_json['result']:
        if(item['phase'] == "BEFORE"):
            lenco = timedelta( seconds =item['durationSeconds'])
            st = datetime.utcfromtimestamp(item['startTimeSeconds']) + timedelta(minutes=330) #UTC + 330minutes (ie 5:30H)
            et = st+lenco
            x = str(item['id'])
            link = "".join(['https://www.codeforces.com/contests/',x])
            cont = Contest(item['id'],link,item['name'] ,st,et)
            
            insert_cont(cont)
        else:
            break