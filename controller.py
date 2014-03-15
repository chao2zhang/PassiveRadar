import telnetlib
import ConfigParser
import re

__all__ = ['Controller']

HINT_USER = 'User:'
HINT_PASSWORD = 'Password:'
HINT_MORE = '--More-- or (q)uit'
HINT_PROMPT = '(Cisco Controller) >'
MESSAGE_LOGOUT = 'logout'
MESSAGE_CLIENT_SUMMARY = 'show rogue client summary'
MESSAGE_CLIENT_DETAILED = 'show rogue client detailed %s'

RE_MAC = re.compile(r'(\w\w:){5}\w\w')
RE_RSSI = re.compile(r'(?P<rssi>-?\d+) dBm')

class Controller:

    def __init__(self, host):
        self.host = host
        self.tn = telnetlib.Telnet(host)

    def _read_until(self, msg='', timeout=1):
        return self.tn.read_until(msg, timeout)

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
        a = ''
        flag = True
        while flag:
            s = self._read_until(HINT_MORE)
            a += s
            if not s or s.endswith(HINT_PROMPT):
                flag = False
            else:
                self._writeline()
        flag = True
        idx = 0
        lst = []
        while flag:
            r = RE_MAC.search(a, idx)
            if r:
                lst.append(a[r.start():r.end()])
                idx = r.end()
            else:
                flag = False
        return lst

    def rssi(self, mac):
        if mac:
            self._writeline(MESSAGE_CLIENT_DETAILED % mac)
            s = self._read_until(HINT_PROMPT)
            return int(RE_RSSI.search(s).group('rssi'))
        return None