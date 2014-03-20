CREATE TABLE IF NOT EXISTS address (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	address TEXT
);
CREATE TABLE IF NOT EXISTS info (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	cid INTEGER,
	aid INTEGER,
	rssi INTEGER,
	snr INTEGER,
	tag TEXT,
	x REAL,
	y REAL,
	date DATE,
	FOREIGN KEY(cid) REFERENCES address(id),
	FOREIGN KEY(aid) REFERENCES address(id)
);
CREATE INDEX IF NOT EXISTS idx_address ON address(address);
CREATE INDEX IF NOT EXISTS idx_cid ON info(cid);
CREATE INDEX IF NOT EXISTS idx_aid ON info(aid);
CREATE INDEX IF NOT EXISTS idx_date ON info(date);
CREATE INDEX IF NOT EXISTS idx_comb ON info(cid, aid, date);