# Statistics page

import streamlit as st
import requests

st.title("RUMAD 2.0")
st.header("Chatbot")

if st.session_state["logged_in"]:
    st.write(f"Hi, {st.session_state["name"]}! Any questions?\n\n\n")
else:
    st.error("You must be logged in to access this page.")