import streamlit as st
from views import view_clients, view_appointments, view_expenses, view_monthly, view_services

def show():
    tab = st.tabs(["Clients", "Appointments", "Expenses", "Monthly Summary", "Services"])

    with tab[0]:
        view_clients.show_data()
    with tab[1]:
        view_appointments.show_data()
    with tab[2]:
        view_expenses.show_data()
    with tab[3]:
        view_monthly.show_data()
    with tab[4]:
        view_services.show_data()

