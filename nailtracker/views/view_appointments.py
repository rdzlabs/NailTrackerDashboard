import streamlit as st
from datetime import date
from data import fetch_clients, fetch_services, fetch_appointments
from logic import insert_appointment
import pandas as pd

def show_form():
    with st.form("appointment_form"):
        # Fetch clients and services
        clients = fetch_clients.get_all()
        services = fetch_services.get_all()

        # Client selector
        client_options = {f"{c['name']} - @{c['instagram']}": c['client_id'] for c in clients}
        selected = st.selectbox("Select Client", list(client_options.keys()))
        client_id = client_options[selected]

        # Services
        service_options = {f"{s['name']} - ${s['base_price']:.2f}": (s['service_id'], s['base_price']) for s in services}
        selected_services = st.multiselect("Services", list(service_options.keys()))
        selected_ids = [service_options[label][0] for label in selected_services]
        base_total = sum(service_options[label][1] for label in selected_services)

        method = st.selectbox("Payment Method", ["Cash", "Card", "Venmo", "Zelle"])
        extra = st.text_input("Extra Charge", "$0.00")
        tip = st.text_input("Tip", "$0.00")
        notes = st.text_area("Notes")
        appt_date = st.date_input("Appointment Date", value=date.today())

        submitted = st.form_submit_button("Log Appointment")

        def parse_money(val): return float(val.replace("$", "").strip() or 0)

        if submitted:
            insert_appointment.run(
                client_id,
                method,
                base_total,
                parse_money(extra),
                parse_money(tip),
                appt_date,
                notes,
                selected_ids
            )
            st.success("Appointment logged.")

def show_data():
    st.subheader("Appointment History")

    # Fetch all appointments
    appointments = fetch_appointments.get_all()

    # Search
    search = st.text_input("Search by client name...")
    if search:
        appointments = [a for a in appointments if search.lower() in a["client_name"].lower()]

    # Display each row using expanders
    for appt in appointments:
        with st.expander(f"{appt['appointment_date']} — {appt['client_name']} — ${appt['total_amount']:.2f} ({appt['method']})"):
            st.markdown(f"**Services:** {', '.join(appt['services']) or '—'}")
            st.markdown(f"**Notes:** {appt['notes'] or 'No notes'}")
