import sqlite3

conn = sqlite3.connect('scooterbot.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                discord_id TEXT UNIQUE,
                user_name TEXT,
                role TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task_name TEXT UNIQUE,
                task_description TEXT,
                task_contributor TEXT,
                points REAL,
                requires_verification BOOLEAN
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS rewards (
                id INTEGER PRIMARY KEY,
                reward_name TEXT,
                reward_description TEXT,
                reward_contributor TEXT,
                cost REAL,
                reward_rate BOOLEAN
            )''')


c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                transaction_datetime datetime,
                change REAL,
                transaction_reason TEXT,
                transaction_pending BOOLEAN,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )''')

# Create checkouts table
c.execute('''CREATE TABLE IF NOT EXISTS checkouts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                reward_id INTEGER,
                checkout_time DATETIME,
                checkin_time DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(reward_id) REFERENCES rewards(id)
            )''')

conn.commit()
conn.close()