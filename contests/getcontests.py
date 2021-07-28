from contests.contestSites.codechef import get_codechef_contests
from contests.contestSites.leetcode import get_leetcode_contests
from contests.contestSites.codeforces import get_codeforces_contests

def get_upcoming_contests():

    get_codeforces_contests()

    get_codechef_contests()

    get_leetcode_contests()
