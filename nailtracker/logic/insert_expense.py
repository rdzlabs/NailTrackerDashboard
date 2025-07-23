import sqlite3

def run(description: str, amount: float, category: str, purchase_date: str, vendor: str = "unknown"):
    try:
        # Sanitize input
        description = description.strip()
        category = category.strip() or None
        vendor = vendor.strip() or "unknown"

        if not description or amount <= 0:
            return False  # Don't insert blank or invalid amounts

        conn = sqlite3.connect("database/nailtracker.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (description, amount, category, purchase_date, vendor)
            VALUES (?, ?, ?, ?, ?)
        """, (description, amount, category, purchase_date, vendor))

        conn.commit()
        return True
    except Exception as e:
        print("Expense insert failed:", e)
        return False
