import time
from datetime import datetime, timedelta
import asyncio

import discord
from discord.embeds import Embed

from contests.getcontests import get_upcoming_contests
import dscrd.embds as embds
import db.contest_data as contest_data
import db.server_data as server_data

async def set_new_channel(serv : discord.Guild,emb):
    for c in serv.text_channels:
        if (c.permissions_for(serv.me).send_messages==True):
            server_data.insert_serv(serv.id, c.id)
            print('new server data inserted', serv, c,datetime.now())
            await c.send('Your announcement settings has just been changed due to permission issues, announcements will be sent on this channel fom now on.')
            await c.send(embed=emb)
            return
    
    server_data.remove_serv(serv.id)
    print('server removed', serv,datetime.now())
    return

async def send_updates(emb,client : discord.Client):
    await asyncio.sleep(3)
    for serv in client.guilds:
        await client.wait_until_ready()
        await asyncio.sleep(1)
        try:
            c_id = server_data.get_chnl_by_serv(serv.id)
            channel= client.get_channel(int(c_id))
        except:
            channel = None
    
        if channel == None:
            await set_new_channel(serv,emb)
        else:
            try:
                await channel.send(embed=emb)
                print('sending message without problem', channel, datetime.now())
            except:
                await set_new_channel(serv,emb)

    

async def main_updates(client):
    await get_upcoming_contests()

    #aleady sorted by time, has Time_List objects
    time_list = contest_data.get_time_list()

    global next_contest
    for t in time_list:
        if t.char_ == 's' and datetime.now()<t.time_:
            next_contest=contest_data.get_cont_by_id(t.id_)
            break

    timestart=time.time()
    duration = 3600
    while(time.time() < timestart+duration):
        print('inside while')
        for dtime in time_list:
            if( (dtime.time_ -timedelta(hours=28)) < datetime.now() < (dtime.time_ - timedelta(hours=22)) and dtime.day1_rem == False):
                contest_data.update_rd1(dtime.id_)
                dtime.day1_rem = True
                em = embds.embed_1drem(contest_data.get_cont_by_id(dtime.id_))
                print('1d rem sending..',dtime)
                await send_updates(em,client)
            elif( (dtime.time_ -timedelta(minutes=50)) < datetime.now() < (dtime.time_ -timedelta(minutes=2))  and dtime.hour1_rem == False):
                contest_data.update_rh1(dtime.id_)
                dtime.hour1_rem = True
                em = embds.embed_1hrem(contest_data.get_cont_by_id(dtime.id_),client.user.avatar_url)
                print('1h rem sending..',dtime)
                await send_updates(em,client)
            elif(datetime.now() > dtime.time_ and dtime.char_ == 'e'):
                em = embds.embed_contest_ended(contest_data.get_cont_by_id(dtime.id_))
                await send_updates(em,client)
                dtime.char_ = 'x' #garbage value so this dtime do not get to come here again
                print('contest ended..',dtime)
                contest_data.remove_cont(dtime.id_)

        print('outside for sleep 5m .. ')
        await asyncio.sleep(300)
        print(datetime.now())


def get_next_contest():
    return next_contest
