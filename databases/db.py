import sqlite3

db = sqlite3.connect("databases/users.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    name TEXT
)
""")
db.commit()

def add_user(user_id, name):
    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (user_id, name)
    )
    db.commit()

def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )
    return cursor.fetchone()




