import streamlit as st
from views import view_dashboard, view_data

st.set_page_config(page_title="NailTracker", layout="wide")

# Sidebar nav
section = st.sidebar.radio("Navigate", ["Dashboard", "View Data"])

# Section router
if section == "Dashboard":
    st.title("Dashboard")
    view_dashboard.show()

elif section == "View Data":
    st.title("View Data")
    view_data.show()
