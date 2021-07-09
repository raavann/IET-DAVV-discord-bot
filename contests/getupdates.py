from contests.data_class import Time_List
import time
from datetime import datetime, timedelta
import asyncio

import contests.codechef as codechef
import contests.codeforces as codeforces
import dscrd.embds as embds
import db.contest_data as contest_data
import db.server_data as server_data


async def get_updates():
    # [code] -> [link, name, start_T, end_T]
    codechef.create_browser()
    codeforces.create_browser()

    codechef.get_present_contests()

    while(True):
        ###update dict_of_contests and time_list
        codechef.get_upcoming_contests()
        codeforces.get_upcoming_contests()

        #aleady sorted by time, has Time_List objects
        time_list = contest_data.get_time_list()

        if len(time_list)==0:
            print('no contest')
            asyncio.sleep(7200)
            continue

        nearest_contest_time = time_list[0]
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
                    # print('Contest starts tomorrow')
                    
                    contest_data.update_rd1(dtime.id_,True)
                elif( (datetime.now() + timedelta(hours=1)) > dtime.time_  and dtime.hour1_rem == False):
                    print('Contest about to start in an hour')
                    contest_data.update_rh1(dtime.id_,True)
                    time_list.pop(index)
                    break
                elif(datetime.now() > dtime.time_):
                    tempid = dtime.id_
                    time_list.pop(index)               
                    if (dtime.char_ == 'e'):
                        print("Contest ended, how'd you do?")
                        contest_data.remove_cont(tempid)
                    break

                time.sleep(300)

            #exit for loop after 6 hours and check for new contests.
            if(time.time() > time_start+duration):
                break
