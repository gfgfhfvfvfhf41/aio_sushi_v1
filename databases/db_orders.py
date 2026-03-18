import sqlite3
from databases import db
db = sqlite3.connect("databases/orders.db")
cursor = db.cursor()


# таблица заказов
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product TEXT,
    quantity INTEGER,
    delivery_date TEXT,
    created_at TEXT
)
""")
db.commit()

def add_order(user_name, product, quantity, delivery_date, created_at):
    cursor.execute(
        "INSERT INTO orders (user_id, product, quantity, delivery_date, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_name, product, quantity, delivery_date, created_at)
    )
    db.commit()


def get_orders_by_date(date):
    cursor.execute(
        "SELECT id, user_id, product, quantity FROM orders WHERE delivery_date=?",
        (date,)
    )
    return cursor.fetchall()


def delete_order(order_id):
    cursor.execute(
        "DELETE FROM orders WHERE id=?",
        (order_id,)
    )
    db.commit()


def get_all_orders():
    cursor.execute(
        "SELECT id, user_id, product, quantity, delivery_date FROM orders"
    )
    return cursor.fetchall()