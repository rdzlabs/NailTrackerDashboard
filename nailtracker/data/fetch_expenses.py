import sqlite3
from datetime import datetime

def get_available_years():
    conn = sqlite3.connect("database/nailtracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%Y', purchase_date)
        FROM expenses
        ORDER BY 1 DESC
    """)
    return [row[0] for row in cursor.fetchall()]

def get_by_year(year: str = None):
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if not year:
        from datetime import datetime
        year = str(datetime.now().year)

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE strftime('%Y', purchase_date) = ?
        ORDER BY purchase_date DESC
    """, (year,))
    return [dict(row) for row in cursor.fetchall()]
