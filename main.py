import ConfigParser
from controller import Controller

# load config
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
addr = config.get('AP', 'addr')
user = config.get('AP', 'user')
pwd = config.get('AP', 'pass')

ctrl = Controller(addr)
ctrl.login(user, pwd)
clients = ctrl.clients()
for client in clients:
    print client, ctrl.rssi(client)
ctrl.logout()