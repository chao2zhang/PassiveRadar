import telnet
import ConfigParser
import re

__all__ = ['Controller']

HINT_USER = 'User:'
HINT_PASSWORD = 'Password:'
HINT_MORE = 'q)uit'
HINT_PROMPT = 'er) >'
RE_HINT_MORE = re.compile(r'q\)uit$')
RE_HINT_PROMPT = re.compile(r'er\) >$')
MESSAGE_LOGOUT = 'logout'
MESSAGE_CLIENT_SUMMARY = 'show rogue client summary'
MESSAGE_CLIENT_DETAILED = 'show rogue client detailed %s'

RE_MAC = re.compile(r'(\w\w:){5}\w\w')
RE_RSSI = re.compile(r'(?P<rssi>-?\d+) dBm')

class Controller:

    def __init__(self, host):
        self.host = host
        self.tn = telnet.Telnet(host)

    def _read_until(self, msg='', timeout=0.5):
        return self.tn.read_until(msg, timeout)

    def _read_full(self, timeout=0.5):
        s = ''
        last_r = ''
        while True:
            r = self.tn.expect([RE_HINT_MORE, RE_HINT_PROMPT], timeout)
            if last_r:
                r = last_r + r
            s += r[2]
            if r[0] == 0:
                self._writeline()
            if r[0] == -1:
                last_r = r
            else:
                last_r = ''
            if not r[2]:
                break
        return s

    def _writeline(self, msg=''):
        self.tn.write(msg + '\n')

    def login(self, user, password):
        self.user = user
        self.password = password
        self._read_until(HINT_USER)
        self._writeline(user)
        if password:
            self._read_until(HINT_PASSWORD)
            self._writeline(password)

    def logout(self):
        self._writeline(MESSAGE_LOGOUT)
        self.tn.close()

    def clients(self):
        self._writeline(MESSAGE_CLIENT_SUMMARY)
        s = self._read_full()
        idx = 0
        lst = []
        while True:
            r = RE_MAC.search(s, idx)
            if r:
                lst.append(s[r.start():r.end()])
                idx = r.end()
            else:
                break
        return lst

    def rssi(self, mac):
        if mac:
            self._writeline(MESSAGE_CLIENT_DETAILED % mac)
            s = self._read_full()
            r = RE_RSSI.search(s)
            if r:
                return r.group('rssi')
        return None