import sqlite3

# Connect to the database
conn = sqlite3.connect('whatsup.db')
cursor = conn.cursor()

# Create FAQ table
cursor.execute('''
CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT,
    status TEXT CHECK(status IN ('draft', 'published')) NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ FAQ table created successfully in whatsup.db")


