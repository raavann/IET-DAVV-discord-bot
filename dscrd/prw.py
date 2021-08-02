import asyncpraw
import os
import random

cl_id = os.environ['praw_clientid']
cl_sec = os.environ['praw_secret']

def isMeme(submission):
    '''
    Function that checks if the reddit submission is a meme or garbage.

    Parameters:
        submisson: reddit submisson from praw's ListingGenerator
    '''
    if submission.url[-4:-3] == '.':
        return True
    return False

async def send_meme():
    reddit = asyncpraw.Reddit(
        client_id=cl_id,
        client_secret=cl_sec,
        user_agent="raavnnn",
    )

    # list of subreddits from which you wanna get your memes from
    subreddits = ['ProgrammerHumor', 'codinghumor']

    # making subreddit instaces using praw
    subredditInstances = [await reddit.subreddit(subreddit) for subreddit in subreddits]

    # getting subreddit category objects
    subredditCategories = []
    for subredditInstance in subredditInstances:
        subredditCategories += [subredditInstance.controversial, subredditInstance.hot, subredditInstance.new, subredditInstance.rising]

    # selecting random subreddit category
    randomSubredditCategory = random.choice(subredditCategories)

    # storing only image URLs
    memeURLs=[str(submission.url) async for submission in randomSubredditCategory(limit = 20) if not submission.over_18 and isMeme(submission)]

    return random.choice(memeURLs)