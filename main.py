import ConfigParser
from db import RadarDB
from controller import Controller
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tag', help='special tag')
parser.add_argument('--x', type=float, help='x position')
parser.add_argument('--y', type=float, help='y position')
args = parser.parse_args()

# load config
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
addr = config.get('AP', 'addr')
user = config.get('AP', 'user')
pwd = config.get('AP', 'pass')
dbfile = config.get('Database', 'file')

db = RadarDB()
db.connect(dbfile, x=args.x, y=args.y, tag=args.tag)
ctrl = Controller(addr)
ctrl.login(user, pwd)

def get_info(client):
    for i in ctrl.info(client):
        info = [client]
        info += i
        info[2] = int(info[2].split()[0])
        info[3] = int(info[3].split()[0]) if info[3] != 'NA' else None
        info[4] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(info[4]))
        db.add_info(*info)
clients = ctrl.clients()
import time
for i in range(30):
    get_info('b4:07:f9:42:6c:ce')
    db.commit()
    time.sleep(2)
ctrl.logout()
db.close()