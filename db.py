import sqlite3

__all__ = ['RadarDB']

SELECT_ADDRESS_ID = 'SELECT id FROM address WHERE address = ?'
INSERT_ADDRESS = 'INSERT INTO address(address) VALUES (?)'
SELECT_INFO = 'SELECT id FROM info WHERE cid = ? AND aid = ? AND date = ?'
INSERT_INFO = 'INSERT INTO info(cid, aid, rssi, snr, date) VALUES (?, ?, ?, ?, ?)'

class RadarDB:
    def connect(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def add_info(self, client, ap, rssi, snr, date):
        self.c.execute(SELECT_ADDRESS_ID, (client,))
        r = self.c.fetchone()
        if not r:
            self.c.execute(INSERT_ADDRESS, (client,))
            self.c.execute(SELECT_ADDRESS_ID, (client,))
            r = self.c.fetchone()
        client = r[0]
        
        self.c.execute(SELECT_ADDRESS_ID, (ap,))
        r = self.c.fetchone()
        if not r:
            self.c.execute(INSERT_ADDRESS, (ap,))
            self.c.execute(SELECT_ADDRESS_ID, (ap,))
            r = self.c.fetchone()
        ap = r[0]

        self.c.execute(SELECT_INFO, (client, ap, date))
        if not self.c.fetchone():
            self.c.execute(INSERT_INFO, (client, ap, rssi, snr, date))
            
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()