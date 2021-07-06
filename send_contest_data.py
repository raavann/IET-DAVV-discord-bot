import time
from datetime import datetime, timedelta

import contests.codechef as codechef
import contests.codeforces as codeforces

if __name__ == '__main__' :
    # [code] -> [link, name, start_T, end_T]
    codechef.create_browser()
    codeforces.create_browser()
    dict_of_contests = {}   
    time_list = []

    codechef.get_present_contests(dict_of_contests,time_list)

    while(True):
        ###update dict_of_contests and time_list
        codechef.get_upcoming_contests(dict_of_contests,time_list)
        codeforces.get_upcoming_contests(dict_of_contests,time_list)
        time_list.sort(key =lambda t:t.time_)

        #write in log file
        if len(time_list)==0:
            print('nothing found')
            time.sleep(7200)
            continue
        
        for index,dtime in enumerate(time_list):
            time_start = time.time()
            duration = 21600
            #while loop runs for 6 hours at max
            while(time.time() < time_start+duration):
                if( (datetime.now() + timedelta(days=1)) > dtime.time_ and dtime.char_ =='s' and dict_of_contests[dtime.id_][0].day1_rem == False):
                    print('Contest starts tomorrow')
                    dict_of_contests[dtime.id_][0].day1_rem = True
                elif( (datetime.now() + timedelta(hours=1)) > dtime.time_ and dtime.char_ =='s' and dict_of_contests[dtime.id_][0].hour1_rem == False):
                    print('Contest about to start in an hour')
                    dict_of_contests[dtime.id_][0].hour1_rem = True
                    time_list.pop(index)
                    break
                elif(datetime.now() > dtime.time_):
                    time_list.pop(index)               
                    if (dtime.char_ == 'e'):
                        print("Contest ended, how'd you do?")
                        dict_of_contests.pop(dtime.id_)
                    break

                time.sleep(300)

            #exit for loop after 6 hours and check for new contests.
            if(time.time() > time_start+duration):
                break
