import streamlit as st
from logic import insert_client


def show_form():
    with st.form("add_client_form"):
        name = st.text_input("Name")
        instagram = st.text_input("Instagram")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Client")

        if submitted:
            insert_client.run(name, phone, email, instagram)
            st.success("Client added.")
