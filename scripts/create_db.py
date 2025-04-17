import sqlite3

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('my_database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a new table (you can change the schema as needed)
cursor.execute('''
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    steps INTEGER DEFAULT 0,
    minutes_running INTEGER DEFAULT 0,
    minutes_cycling INTEGER DEFAULT 0,
    minutes_swimming INTEGER DEFAULT 0,
    minutes_exercise INTEGER DEFAULT 0,
    calories INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
''')

# Commit changes
conn.commit()

# Close the connection
conn.close()

print("Database and table created successfully.")