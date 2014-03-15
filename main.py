import ConfigParser
from controller import Controller

# load config
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
addr = config.get('AP', 'addr')
user = config.get('AP', 'user')
pwd = config.get('AP', 'pass')

c = Controller(addr)
c.login(user, pwd)
print c.summary()
c.logout()