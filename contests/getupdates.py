from contests.data_class import Time_List
import time
from datetime import datetime, timedelta
import asyncio

import contests.codechef as codechef
import contests.codeforces as codeforces
import dscrd.embds as embds
import db.contest_data as contest_data
import db.server_data as server_data
from discord import client
import dscrd.embds as embds

async def send_updates(emb,client):
    for c_id in server_data.get_all_chnls():
        channel= client.get_channel(int(c_id))
        await channel.send(embed=emb)

async def get_updates(client):
    # [code] -> [link, name, start_T, end_T]
    codechef.create_browser()
    codeforces.create_browser()

    codechef.get_present_contests()

    while(True):
        codechef.get_upcoming_contests()
        codeforces.get_upcoming_contests()

        #aleady sorted by time, has Time_List objects
        time_list = contest_data.get_time_list()

        if len(time_list)==0:
            print('no contest')
            asyncio.sleep(7200)
            continue

        nearest_contest_time = time_list[0].time_
        until_update = nearest_contest_time-datetime.now()
        rd1 = contest_data.get_rd1_by_id(time_list[0].id_)
        rh1 = contest_data.get_rh1_by_id(time_list[0].id_)

        if(until_update > timedelta(days=1) and rd1==False):
            st = min(timedelta(hours=6), until_update-timedelta(days=1))
            await asyncio.sleep(st)
        elif(until_update > timedelta(hours=1) and rh1==False):
            st = min(timedelta(hours=6),until_update-timedelta(hours=1))
            await asyncio.sleep(st)
        
        for index,dtime in enumerate(time_list):
            time_start = time.time()
            duration = 21600
            #while loop runs for 6 hours at max
            while(time.time() < time_start+duration):
                if( (datetime.now() + timedelta(days=1)) > dtime.time_  and dtime.day1_rem == False):
                    contest_data.update_rd1(dtime.id_,True)
                    dtime.day1_rem = True
                    await send_updates(embds.embed_1drem(contest_data.get_cont_by_id(dtime.id_),client.user.avatar_url),client)
                elif( (datetime.now() + timedelta(hours=1)) > dtime.time_  and dtime.hour1_rem == False):
                    contest_data.update_rh1(dtime.id_,True)
                    dtime.hour1_rem = True
                    await send_updates(embds.embed_1hrem(contest_data.get_cont_by_id(dtime.id_),client.user.avatar_url),client)
                    time_list.pop(index)
                    break
                elif(datetime.now() > dtime.time_):
                    tempid = dtime.id_
                    time_list.pop(index)               
                    if (dtime.char_ == 'e'):
                        await send_updates(embds.embed_contest_ended(contest_data.get_cont_by_id(dtime.id_)),client)
                        contest_data.remove_cont(tempid)
                    break

                await asyncio.sleep(300)

            #exit for loop after 6 hours and check for new contests.
            if(time.time() > time_start+duration):
                break
