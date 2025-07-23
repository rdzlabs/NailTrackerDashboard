import streamlit as st
import pandas as pd
from data import fetch_services

def show_data():
    st.subheader("Service Stats")

    # Year filter
    years = fetch_services.get_available_years()
    selected_year = st.selectbox("Select Year", years, key="year_services")

    # Get service stats
    services = fetch_services.get_summary_by_year(selected_year)

    # Format table
    rows = [
        {
            "Service": s["name"],
            "Base Price": f"${s['base_price']:,.2f}",
            "Times Used": s["times_used"],
            "Total Revenue": f"${s['total_revenue']:,.2f}",
        }
        for s in services
    ]

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
