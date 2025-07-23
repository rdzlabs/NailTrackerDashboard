import sqlite3
from datetime import datetime

def get_available_years():
    conn = sqlite3.connect("database/nailtracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%Y', appointment_date) as year
        FROM appointments
        ORDER BY year DESC
    """)
    return [row[0] for row in cursor.fetchall()]

def get_summary_by_year(year: str = None):
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if not year:
        year = str(datetime.now().year)

    query = """
        SELECT 
            c.client_id,
            c.name,
            c.instagram,
            c.phone,
            c.email,
            COUNT(a.appointment_id) AS total_appointments,
            IFNULL(SUM(p.total_amount), 0) AS total_spent
        FROM clients c
        LEFT JOIN appointments a 
            ON c.client_id = a.client_id 
            AND strftime('%Y', a.appointment_date) = ?
        LEFT JOIN payments p ON a.payment_id = p.payment_id
        WHERE a.appointment_id IS NOT NULL
        GROUP BY c.client_id
        ORDER BY total_spent DESC
    """
    cursor.execute(query, (year,))
    return [dict(row) for row in cursor.fetchall()]

def get_all():
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT client_id, name, instagram, phone, email
        FROM clients
        ORDER BY name
    """)
    return [dict(row) for row in cursor.fetchall()]