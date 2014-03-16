import ConfigParser
from db import RadarDB
from controller import Controller
import time

# load config
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
addr = config.get('AP', 'addr')
user = config.get('AP', 'user')
pwd = config.get('AP', 'pass')
dbfile = config.get('Database', 'file')

db = RadarDB()
db.connect(dbfile)
ctrl = Controller(addr)
ctrl.login(user, pwd)
clients = ctrl.clients()
for client in clients:
    for i in ctrl.info(client):
        info = [client]
        info += i
        info[2] = int(info[2].split()[0])
        info[3] = int(info[3].split()[0]) if info[3] != 'NA' else None
        info[4] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(info[4]))
        print info
        db.add_info(*info)
ctrl.logout()
db.commit()
db.close()