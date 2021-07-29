from contests.contestSites.codechef import get_codechef_contests
from contests.contestSites.leetcode import get_leetcode_contests
from contests.contestSites.codeforces import get_codeforces_contests

import asyncio
async def get_upcoming_contests():
    await asyncio.sleep(3)
    await get_codeforces_contests()

    await asyncio.sleep(3)
    await get_codechef_contests()

    await asyncio.sleep(3)
    await get_leetcode_contests()
