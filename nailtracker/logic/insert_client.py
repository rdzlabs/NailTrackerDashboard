import sqlite3

def run(name: str, phone: str, email: str, instagram: str):
    name = name.strip()
    phone = phone.strip()
    email = email.strip() or "none"
    instagram = instagram.strip() or "none"

    if not name:
        return False  # Don't insert blank names

    conn = sqlite3.connect("database/nailtracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clients (name, phone, email, instagram)
        VALUES (?, ?, ?, ?)
    """, (name, phone, email, instagram))

    conn.commit()
    return True
