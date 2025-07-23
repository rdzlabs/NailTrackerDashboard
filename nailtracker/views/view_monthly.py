import streamlit as st
import calendar
import pandas as pd
from data import fetch_monthly

def show_data():
    st.subheader("Monthly Overview")

    years = fetch_monthly.get_available_years()
    selected_year = st.selectbox("Select Year", years, key="year_monthly")

    income_data, expense_data = fetch_monthly.get_summary_by_year(selected_year)

    # Yearly totals
    yearly_income = sum(data["income"] for data in income_data.values())
    yearly_expenses = sum(expense_data.values())
    yearly_profit = yearly_income - yearly_expenses

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Total Income:** ${yearly_income:,.2f}")
    col2.markdown(f"**Total Expenses:** ${yearly_expenses:,.2f}")
    col3.markdown(f"**Net Profit:** ${yearly_profit:,.2f}")



    # Table data
    rows = []
    for m in range(1, 13):
        month_str = f"{m:02}"
        name = calendar.month_name[m]

        appts = income_data.get(month_str, {}).get("appointments", 0)
        income = income_data.get(month_str, {}).get("income", 0)
        expenses = expense_data.get(month_str, 0)
        net = income - expenses

        rows.append({
            "Month": name,
            "Appointments": appts,
            "Income": f"${income:,.2f}",
            "Expenses": f"${expenses:,.2f}",
            "Net Profit": f"${net:,.2f}",
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
