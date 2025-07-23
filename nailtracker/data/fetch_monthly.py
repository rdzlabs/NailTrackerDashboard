import sqlite3
from datetime import datetime
from collections import defaultdict

def get_available_years():
    conn = sqlite3.connect("database/nailtracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT strftime('%Y', appointment_date) AS year
        FROM appointments
        ORDER BY year DESC
    """)
    return [row[0] for row in cursor.fetchall()]

def get_summary_by_year(year: str):
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Appointments + income per month
    cursor.execute("""
        SELECT 
            strftime('%m', a.appointment_date) AS month,
            COUNT(a.appointment_id) AS appointments,
            SUM(p.total_amount) AS income
        FROM appointments a
        JOIN payments p ON a.payment_id = p.payment_id
        WHERE strftime('%Y', a.appointment_date) = ?
        GROUP BY month
    """, (year,))
    income_data = {row["month"]: {"appointments": row["appointments"], "income": row["income"] or 0} for row in cursor.fetchall()}

    # Expenses per month
    cursor.execute("""
        SELECT 
            strftime('%m', purchase_date) AS month,
            SUM(amount) AS expenses
        FROM expenses
        WHERE strftime('%Y', purchase_date) = ?
        GROUP BY month
    """, (year,))
    expense_data = {row["month"]: row["expenses"] or 0 for row in cursor.fetchall()}

    return income_data, expense_data
