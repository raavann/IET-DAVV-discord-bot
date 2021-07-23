import time
from datetime import datetime, timedelta
import asyncio

import contests.codechef as codechef
import contests.codeforces as codeforces
import dscrd.embds as embds
import db.contest_data as contest_data
import db.server_data as server_data
import dscrd.embds as embds

async def send_updates(emb,client):
    for c_id in server_data.get_all_chnls():
        channel= client.get_channel(int(c_id))
        await channel.send(embed=emb)

async def get_updates(client):
    # [code] -> [link, name, start_T, end_T]
    codechef.create_browser()

    while(True):
        codechef.get_upcoming_contests()
        codeforces.get_upcoming_contests()

        #aleady sorted by time, has Time_List objects
        time_list = contest_data.get_time_list()

        if len(time_list)==0:
            print('no contest')
            asyncio.sleep(7200)
            continue

        timestart=time.time()
        duration = 3600
        while(time.time() < timestart+duration):
            print('inside while')
            for dtime in time_list:
                print(dtime)
                if( (dtime.time_ -timedelta(hours=28)) < datetime.now() < (dtime.time_ - timedelta(hours=22)) and dtime.day1_rem == False):
                    contest_data.update_rd1((dtime.id_))
                    dtime.day1_rem = True
                    em = embds.embed_1drem(contest_data.get_cont_by_id((dtime.id_)),client.user.avatar_url)
                    print('1d rem sending..',dtime)
                    await send_updates(em,client)
                elif( (dtime.time_ -timedelta(minutes=50)) < datetime.now() < (dtime.time_ -timedelta(minutes=2))  and dtime.hour1_rem == False):
                    contest_data.update_rh1((dtime.id_))
                    dtime.hour1_rem = True
                    em = embds.embed_1hrem(contest_data.get_cont_by_id((dtime.id_)),client.user.avatar_url)
                    print('1h rem sending..',dtime)
                    await send_updates(em,client)
                elif(datetime.now() > dtime.time_ and dtime.char_ == 'e'):
                    em = embds.embed_contest_ended(contest_data.get_cont_by_id((dtime.id_)))
                    await send_updates(em,client)
                    dtime.char_ = 'x' #garbage value so this dtime do not get to come here again
                    print('contest ended..',dtime)
                    contest_data.remove_cont((dtime.id_))

            print('outside for sleep 5m .. ')
            await asyncio.sleep(300)
            print(datetime.now())
