import sqlite3
from datetime import datetime

def get_available_years():
    conn = sqlite3.connect("database/nailtracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%Y', appointment_date) AS year
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
            s.name,
            s.base_price,
            COUNT(CASE WHEN strftime('%Y', a.appointment_date) = ? THEN aps.id END) AS times_used,
            SUM(CASE WHEN strftime('%Y', a.appointment_date) = ? THEN s.base_price ELSE 0 END) AS total_revenue
        FROM services s
        LEFT JOIN appointment_services aps ON s.service_id = aps.service_id
        LEFT JOIN appointments a ON aps.appointment_id = a.appointment_id
        GROUP BY s.service_id
        ORDER BY total_revenue DESC
    """
    cursor.execute(query, (year, year))
    return [dict(row) for row in cursor.fetchall()]

def get_all():
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT service_id, name, base_price
        FROM services
        ORDER BY name
    """)
    return [dict(row) for row in cursor.fetchall()]
