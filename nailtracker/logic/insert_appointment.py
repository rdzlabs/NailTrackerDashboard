import sqlite3

def run(client_id: int, method: str, base_amount: float, extra_charge: float, tip: float,
        appointment_date: str, notes: str, service_ids: list[int]):
    try:
        conn = sqlite3.connect("database/nailtracker.db")
        cursor = conn.cursor()

        total_amount = base_amount + extra_charge + tip

        # Start transaction
        conn.execute("BEGIN")

        # Insert into payments
        cursor.execute("""
            INSERT INTO payments (method, base_amount, extra_charge, tip, total_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (method, base_amount, extra_charge, tip, total_amount))
        payment_id = cursor.lastrowid

        # Insert into appointments
        cursor.execute("""
            INSERT INTO appointments (client_id, payment_id, appointment_date, notes)
            VALUES (?, ?, ?, ?)
        """, (client_id, payment_id, appointment_date, notes))
        appointment_id = cursor.lastrowid

        # Insert into appointment_services
        if service_ids:
            cursor.executemany(
                "INSERT INTO appointment_services (appointment_id, service_id) VALUES (?, ?)",
                [(appointment_id, sid) for sid in service_ids]
            )

        # Commit transaction
        conn.commit()
        return True
    except Exception as e:
        print("Insert failed:", e)
        conn.rollback()
        return False
