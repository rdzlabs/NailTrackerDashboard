import streamlit as st
import pandas as pd
from data import fetch_clients
from logic import insert_client


def show_form():
    with st.form("client_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        instagram = st.text_input("Instagram")
        submitted = st.form_submit_button("Add Client")

        if submitted:
            success = insert_client.run(name, phone, email, instagram)
            if success:
                st.success("Client added.")
            else:
                st.error("Name is required.")

def show_data():
    st.subheader("Client History")

    # Year selector
    years = fetch_clients.get_available_years()
    selected_year = st.selectbox("Select Year", years, key="year_clients")

    # Fetch client summary for selected year
    clients = fetch_clients.get_summary_by_year(selected_year)

    # Search input
    search = st.text_input("Search clients...")
    if search:
        clients = [c for c in clients if search.lower() in c['name'].lower() or search.lower() in c['instagram'].lower()]

    # Format for display
    table_data = [
        {
            "Name": c["name"],
            "Instagram": c["instagram"],
            "Phone": c["phone"],
            "Email": c["email"],
            "Appointments": c["total_appointments"],
            "Total Spent": f"${c['total_spent']:.2f}",
            # "Actions": ""  # Placeholder if you want edit/delete later
        }
        for c in clients
    ]

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)
