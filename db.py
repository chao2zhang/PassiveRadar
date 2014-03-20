import sqlite3

__all__ = ['RadarDB']

SELECT_ADDRESS_ID = 'SELECT id FROM address WHERE address = ?'
INSERT_ADDRESS = 'INSERT INTO address(address) VALUES (?)'
SELECT_INFO = 'SELECT id FROM info WHERE cid = ? AND aid = ? AND date = ?'
INSERT_INFO = 'INSERT INTO info(cid, aid, rssi, snr, date, tag, x, y) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

class RadarDB:
    def connect(self, db_file, x=0, y=0, tag=None):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.x = x
        self.y = y
        self.tag = tag

    def add_info(self, client, ap, rssi, snr, date):
        self.c.execute(SELECT_ADDRESS_ID, (client,))
        r = self.c.fetchone()
        if not r:
            self.c.execute(INSERT_ADDRESS, (client,))
            self.c.execute(SELECT_ADDRESS_ID, (client,))
            r = self.c.fetchone()
        cid = r[0]
        
        self.c.execute(SELECT_ADDRESS_ID, (ap,))
        r = self.c.fetchone()
        if not r:
            self.c.execute(INSERT_ADDRESS, (ap,))
            self.c.execute(SELECT_ADDRESS_ID, (ap,))
            r = self.c.fetchone()
        aid = r[0]

        self.c.execute(SELECT_INFO, (cid, aid, date))
        if not self.c.fetchone():
            print client, ap, rssi, snr, date, cid, aid
            self.c.execute(INSERT_INFO, (cid, aid, rssi, snr, date, self.tag, self.x, self.y))
            
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()