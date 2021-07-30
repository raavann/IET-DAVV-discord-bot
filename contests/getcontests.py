from contests.contestSites.codechef import get_codechef_contests
from contests.contestSites.leetcode import get_leetcode_contests
from contests.contestSites.codeforces import get_codeforces_contests
from datetime import datetime
import asyncio
async def get_upcoming_contests():
    
    await asyncio.sleep(3)
    try:
        get_codeforces_contests()
        await asyncio.sleep(3)
    except:
        print('problem in codeforces', datetime.now() )

    try:
        await get_codechef_contests()
        await asyncio.sleep(3)
    except:
        print('problem in codechef', datetime.now() )

    try:
        await get_leetcode_contests()
        await asyncio.sleep(5)
    except:
        print('problem in leetcode', datetime.now() )
      