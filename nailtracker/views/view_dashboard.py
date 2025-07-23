import streamlit as st
from views import view_clients, view_appointments, view_expenses


def show():
    tab = st.tabs(["Add Client", "Log Appointment", "Log Expense"])

    with tab[0]:
        view_clients.show_form()

    with tab[1]:
        view_appointments.show_form()

    with tab[2]:
        view_expenses.show_form()
