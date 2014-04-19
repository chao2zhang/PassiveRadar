import sqlite3

__all__ = ['RadarDB']

SELECT_ADDRESS_ID = 'SELECT id FROM address WHERE address = ?'
INSERT_ADDRESS = 'INSERT INTO address(address) VALUES (?)'
SELECT_INFO = 'SELECT id FROM info WHERE client = ? AND ap = ? AND date = ?'
INSERT_INFO = 'INSERT INTO info(client, ap, rssi, snr, date, tag, x, y) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

class RadarDB:
    def connect(self, db_file, x=0, y=0, tag=None):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.x = x
        self.y = y
        self.tag = tag

    def add_info(self, client, ap, rssi, snr, date):
        self.c.execute(SELECT_INFO, (client, ap, date))
        if not self.c.fetchone():
            print client, ap, rssi, snr, date
            self.c.execute(INSERT_INFO, (client, ap, rssi, snr, date, self.tag, self.x, self.y))
            
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()