import telnet
import ConfigParser
import re
import time

__all__ = ['Controller']

HINT_USER = 'User:'
HINT_PASSWORD = 'Password:'
HINT_MORE = 'q)uit'
HINT_PROMPT = 'er) >'
HINT_NEXT = (HINT_MORE, HINT_PROMPT)
MESSAGE_LOGOUT = 'logout'
MESSAGE_CLIENT_SUMMARY = 'show rogue client summary'
MESSAGE_CLIENT_DETAILED = 'show rogue client detailed %s'

RE_MAC = re.compile(r'(\w\w:){5}\w\w', re.L)
RE_MAC_ADDR = re.compile(r'MAC Address\.+ (?P<x>.+)', re.L)
RE_SNR = re.compile(r'SNR\.+ (?P<x>.+)', re.L)
RE_RSSI = re.compile(r'RSSI\.+ (?P<x>.+)', re.L)
RE_LAST_REPORT = re.compile(r'Last reported by this AP\.+ (?P<x>.+)', re.L)

class Controller:

    def __init__(self, host):
        self.host = host
        self.tn = telnet.RawqTelnet(host, timeout=1000)

    def _read_until(self, msg=''):
        return str(self.tn.read_until(msg))

    def _read_full(self):
        s = bytearray()
        while True:
            r = self.tn.read_until(HINT_NEXT)
            s += r[1]
            if r[0] == 0:
                self._writeline()
            else:
                break
        return str(s)

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
        self._read_full()

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

    def info(self, mac):
        result = []
        if mac:
            self._writeline(MESSAGE_CLIENT_DETAILED % mac)
            s = self._read_full()
            i = 1
            r = s.find('AP %i' % i)
            while r > -1:
                try:
                    mac_addr = RE_MAC_ADDR.search(s, r).group('x').strip()
                    rssi = RE_RSSI.search(s, r).group('x').strip()
                    snr = RE_SNR.search(s, r).group('x').strip()
                    last_report = RE_LAST_REPORT.search(s, r).group('x').strip()
                    result.append((mac_addr, rssi, snr, last_report))
                except AttributeError as e:
                    continue
                finally:
                    i += 1
                    r = s.find('AP %i' % i)
        return result