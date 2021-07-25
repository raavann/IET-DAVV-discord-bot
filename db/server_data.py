import sqlite3
con = sqlite3.connect('server.db')

cur = con.cursor()

try:
    cur.execute('''CREATE TABLE server_data(
        server_id integer Primary key,
        channel_id integer
    )
    ''')
except:
    print('table already exists')


def insert_serv(serv,chnl):
    with con:
        cur.execute("INSERT INTO server_data VALUES (:server_id, :channel_id)", {'server_id': serv, 'channel_id': chnl })

def get_chnl_by_serv(serv):
    cur.execute("SELECT channel_id FROM server_data WHERE server_id=:serv", {'serv': serv})
    #returns integer value
    return cur.fetchone()[0]

def get_serv_by_chnl(chnl):
    cur.execute("SELECT server_id FROM server_data WHERE channel_id=:chnl", {'chnl': chnl})
    #returns integer value
    return cur.fetchone()[0]

def update_serv(serv, chnl):
    with con:
        cur.execute("""UPDATE server_data SET channel_id = :chnl
                    WHERE server_id = :serv""",
                  {'chnl': chnl, 'serv': serv})

def remove_serv(serv):
    with con:
        cur.execute("DELETE from server_data WHERE server_id = :serv",
                  {'serv': serv})

#return list of all channels
def get_all_chnls():
    cur.execute("SELECT channel_id FROM server_data")
    ret=[]
    for lt in cur.fetchall():
        ret.append(lt[0])
    return ret