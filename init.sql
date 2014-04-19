CREATE TABLE IF NOT EXISTS info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT,
    ap TEXT,
    tag TEXT,
    rssi INTEGER,
    snr INTEGER,
    x REAL,
    y REAL,
    date DATE
);
CREATE INDEX IF NOT EXISTS idx_comb ON info(client, ap, date);