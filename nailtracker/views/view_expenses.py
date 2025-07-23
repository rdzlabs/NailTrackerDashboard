import streamlit as st
from datetime import date
from logic import insert_expense
import pandas as pd
from data import fetch_expenses

def show_form():

    with st.form("expense_form"):
        desc = st.text_input("Description")
        amount = st.text_input("Amount", "$0.00")
        category = st.text_input("Category")
        vendor = st.text_input("Vendor")
        date_purchased = st.date_input("Purchase Date", date.today())

        submitted = st.form_submit_button("Add Expense")
        if submitted:
            try:
                amt = float(amount.replace("$", "").strip())
                success = insert_expense.run(desc, amt, category, str(date_purchased), vendor)
                if success:
                    st.success("Expense logged.")
                else:
                    st.error("Failed to log expense. Check your inputs.")
            except ValueError:
                st.error("Amount must be a valid number.")

def show_data():
    st.subheader("Expense History")

    # Year selector
    years = fetch_expenses.get_available_years()
    selected_year = st.selectbox("Select Year", years, key="year_expenses")

    # Fetch expenses for that year
    expenses = fetch_expenses.get_by_year(selected_year)

    # Total summary
    total = sum(e["amount"] for e in expenses)
    st.markdown(f"**Total Expenses in {selected_year}:** ${total:,.2f}")

    # Search
    search = st.text_input("Search expenses...")
    if search:
        expenses = [e for e in expenses if search.lower() in e["description"].lower() or search.lower() in e["vendor"].lower()]

    # Format table
    rows = [
        {
            "Date": e["purchase_date"],
            "Category": e["category"] or "—",
            "Description": e["description"],
            "Vendor": e["vendor"],
            "Amount": f"${e['amount']:,.2f}",
        }
        for e in expenses
    ]

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
