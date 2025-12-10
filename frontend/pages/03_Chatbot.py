# Chatbot page

import streamlit as st
import time
import requests

# MAKE SURE TO RUN MAIN LOCALLY BEFORE
# API_BASE = "http://127.0.0.1:5000/Fulcrum/api"
API_BASE = st.secrets["api"]["local_url"]

st.title("RUMAD 2.0")
st.header("Chatbot")

if st.session_state["logged_in"]:

    if "messages" not in st.session_state or st.session_state["messages"] == []:
        st.session_state.messages = [{"role": "assistant", "content": f"Hi, {st.session_state["name"]}! Any questions?"}]

    # Show existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a question about course syllabi."):
        history_for_call = [{"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.messages]

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Calling API (local)
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json = {
                    "question": prompt,
                    "history": history_for_call,
                },
                timeout=120,
            )

            try:
                data = response.json()
            except ValueError:
                data = None

            if response.status_code == 200 and data is not None:
                answer = data.get("answer", "No answer from chatbot API.")
            else:
                if isinstance(data, dict):
                    error_msg = data.get("details") or data.get("error") or str(data)
                else:
                    error_msg = response.text
                answer = f"Chatbot API error ({response.status_code}): {error_msg}"

        except requests.RequestException as e:
            answer = f"Error with chatbot API: {e}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Simulate stream of response with milliseconds delay
            for chunk in answer.split():
                full_response += chunk + " "
                time.sleep(0.05)

                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response.strip()})
else:
    st.error("You must be logged in to access this page.")