import asyncpraw
import os
import random

cl_id = os.environ['praw_clientid']
cl_sec = os.environ['praw_secret']

async def send_meme():
    reddit = asyncpraw.Reddit(
        client_id=cl_id,
        client_secret=cl_sec,
        user_agent="raavnnn",
    )

    meme_1 = await reddit.subreddit('ProgrammerHumor')
    meme_2 = await reddit.subreddit('codinghumor')

    options = [meme_1.controversial, meme_1.hot, meme_1.new, meme_1.rising,
        meme_1.top, meme_2.controversial, meme_2.hot, meme_2.new, meme_2.rising, meme_2.top]

    choosen = random.choice(options)
    urls=[]
    async for item in choosen(limit=10):
        if(item.url[-4:-3] == '.'):
            urls.append(str(item.url))

    return random.choice(urls)