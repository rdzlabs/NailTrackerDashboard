import streamlit as st
from views import view_clients, view_appointments, view_expenses

def show():
    tab = st.tabs(["Clients", "Appointments", "Expenses", "Monthly Summary"])

    with tab[0]:
        view_clients.show_data()

    with tab[1]:
        view_appointments.show_data()

    with tab[2]:
        view_expenses.show_data()

    with tab[3]:
        st.write("Monthly summary coming soon...")
