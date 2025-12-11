# Landing log in page

import streamlit as st
import requests

def authenticate_user(username, password):
    url = f"{st.secrets["api"]["base_url"]}/auth"
    auth_json = {
        "username": username,
        "password": password
    }

    response = requests.get(url=url, json=auth_json)

    if response.status_code == 200:
        return response.json()["name"]
    else:
        return False

def login_page():
    st.header("Log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_pressed = st.button("Login")

    if login_pressed:
        name = authenticate_user(username, password)
        if name:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.success("Successfully logged in")
            st.switch_page("pages/02_Statistics.py")
        else:
            st.error("Invalid username or password")

def logout_page():
    st.header("Log out")

    logout_pressed = st.button("Log out")

    if logout_pressed:
        # Reset states
        if "logged_in" in st.session_state:
            st.session_state.logged_in = False
        if "name" in st.session_state:
            st.session_state.name = None
        if "messages" in st.session_state:
            st.session_state.messages = []
        history_for_call = []
        prompt = None
        response = None
        data = None
        answer = None
        message_placeholder = None
        full_response = None

        st.success("Successfully logged out")
        st.rerun()

# Start logged out
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("RUMAD 2.0")

# Call
if not st.session_state.logged_in:
    login_page()
else:
    logout_page()