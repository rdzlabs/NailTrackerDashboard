import streamlit as st
from datetime import date
from logic import insert_expense

def show_form():
    with st.form("expense_form"):
        desc = st.text_input("Description")
        amount = st.text_input("Amount", "$0.00")
        category = st.text_input("Category")
        vendor = st.text_input("Vendor")
        date_purchased = st.date_input("Purchase Date", date.today())
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            amt = float(amount.replace("$", "").strip() or 0)
            insert_expense.run(desc, amt, category, date_purchased, vendor)
            st.success("Expense logged.")
