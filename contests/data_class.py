from dataclasses import dataclass
from datetime import datetime

@dataclass
class Contest:
    id: str
    link: str
    name: str
    start_time: datetime
    end_time: datetime
    day1_rem: bool= False #check if 1 day is remaining for contest
    hour1_rem: bool=False #check if 1 hour is remaining for contest

@dataclass
class Time_List:
    time_ : datetime #start time and endtime
    char_ : str         #'s' is starttime, 'e' is endtime
    id_ : str           #contest-id
    day1_rem :bool
    hour1_rem: bool