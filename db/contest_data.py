import sqlite3
from contests.data_class import Time_List
from contests.data_class import Contest


con = sqlite3.connect('contest.db',detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("bool", lambda v: bool(int(v)))

try:
    cur.execute('''CREATE TABLE contest_data(
        id text primary key,
        link text,
        name text,
        start_time timestamp,
        end_time timestamp,
        day1_rem bool,
        hour1_rem bool,
        UNIQUE (id,start_time)
    )
    ''')
except:
    print('table exists')

#inserts into database via Contest object
def insert_cont(cont):
    try:
        with con:
            cur.execute("INSERT INTO contest_data VALUES (:id, :link,:name,:st,:et,:d1,:h1)", {'id': cont.id, 'link': cont.link,'name':cont.name,'st':cont.start_time,'et':cont.end_time,'d1':cont.day1_rem,'h1':cont.hour1_rem })
    except:
        with con:
            cur.execute("UPDATE contest_data SET start_time=:st, end_time=:et WHERE id = :id",{'st':cont.start_time,'et':cont.end_time, 'id':cont.id})
    
#return Contest object
def get_cont_by_id(id):
    cur.execute("SELECT id,link,name,start_time,end_time,day1_rem,hour1_rem FROM contest_data WHERE id=:id", {'id': id})
    dt = cur.fetchone()
    if (dt == None):
        return None
    else:
        cont = Contest(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6])
        return cont
        # return Contest(*cur.fetchone())

#create time list of Time_List object sorts it and send it
def get_time_list():
    cur.execute("SELECT start_time,end_time,id,day1_rem,hour1_rem FROM contest_data")
    timelist=[]
    for t in cur.fetchall():
        timelist.append(Time_List(t[0],'s',t[2],t[3],t[4]))
        timelist.append(Time_List(t[1],'e',t[2],True,True))
    
    timelist.sort(key =lambda t:t.time_)
    return timelist

def get_rd1_by_id(id):
    cur.execute("SELECT day1_rem FROM contest_data WHERE id=:id", {'id': id})
    return cur.fetchone()[0]


def get_rh1_by_id(id):
    cur.execute("SELECT hour1_rem FROM contest_data WHERE id=:id", {'id': id})
    return cur.fetchone()[0]

def update_rd1(id):
    with con:
        cur.execute("""UPDATE contest_data SET day1_rem = :val WHERE id = :id""",{'val':True, 'id': id})

def update_rh1(id):
    with con:
        cur.execute("""UPDATE contest_data SET hour1_rem = :val WHERE id = :id""",{'val': True, 'id': id})

def remove_cont(id):
    with con:
        cur.execute("DELETE from contest_data WHERE id = :id",
                  {'id': id})
