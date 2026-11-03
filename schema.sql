DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS matches;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL, -- 'donor' or 'hospital'
    blood_type TEXT,
    organ_type TEXT,
    medical_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER NOT NULL,
    hospital_id INTEGER NOT NULL,
    organ_type TEXT NOT NULL,
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(donor_id) REFERENCES users(id),
    FOREIGN KEY(hospital_id) REFERENCES users(id)
);
