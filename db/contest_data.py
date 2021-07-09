import sqlite3
from contests.data_class import Time_List
from contests.data_class import Contest


con = sqlite3.connect('database.db',detect_types=sqlite3.PARSE_DECLTYPES)
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
        rem_1d bool,
        rem_1h bool
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
        print('contest already exist')

#return Contest object
def get_cont_by_id(id):
    cur.execute("SELECT id,link,name,start_time,end_time,rem_1d,rem_1h FROM contest_data WHERE id=:id", {'id': id})
    dt = cur.fetchone()
    if (dt == None):
        return None
    else:
        return Contest(*cur.fetchone())

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
    cur.execute("SELECT rem_1d FROM contest_data WHERE id=:id", {'id': id})
    return cur.fetchone()[0]


def get_rh1_by_id(id):
    cur.execute("SELECT rem_1h FROM contest_data WHERE id=:id", {'id': id})
    return cur.fetchone()[0]

def update_rd1(id,val):
    with con:
        cur.execute("""UPDATE contest_data SET rem_1d = :val WHERE id = :id""",{'val': val, 'id': id})

def update_rh1(id,val):
    with con:
        cur.execute("""UPDATE contest_data SET rem_1h = :val WHERE id = :id""",{'val': val, 'id': id})

def remove_cont(id):
    with con:
        cur.execute("DELETE from contest_data WHERE id = :id",
                  {'id': id})