import sqlite3

def get_all():
    conn = sqlite3.connect("database/nailtracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch main appointment info
    cursor.execute("""
        SELECT 
            a.appointment_date,
            c.name AS client_name,
            p.total_amount,
            p.method,
            a.notes,
            a.appointment_id
        FROM appointments a
        JOIN clients c ON a.client_id = c.client_id
        JOIN payments p ON a.payment_id = p.payment_id
        ORDER BY a.appointment_date DESC
    """)
    appointments = [dict(row) for row in cursor.fetchall()]

    # Fetch all services per appointment
    cursor.execute("""
        SELECT aps.appointment_id, s.name
        FROM appointment_services aps
        JOIN services s ON aps.service_id = s.service_id
    """)
    service_map = {}
    for row in cursor.fetchall():
        appt_id = row["appointment_id"]
        service_map.setdefault(appt_id, []).append(row["name"])

    # Attach services to appointments
    for appt in appointments:
        appt_id = appt["appointment_id"]
        appt["services"] = service_map.get(appt_id, [])

    return appointments
