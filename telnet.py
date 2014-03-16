from telnetlib import Telnet

class RawqTelnet(Telnet):
    def read_until(self, match):
        b = bytearray()
        if hasattr(match, '__iter__'):
            while not self.eof:
                for i in range(len(match)):
                    if b.endswith(match[i]):
                        return (i, b)
                b.append(self.rawq_getchar())
            return (-1, b)
        else:
            while not self.eof and not b.endswith(match):
                b.append(self.rawq_getchar())
        return b