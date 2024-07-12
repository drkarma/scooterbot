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
                cost REAL
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

conn.commit()
conn.close()