import streamlit as st
import requests

st.title("AI Agent Chatbot")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Bạn:", "")

if st.button("Gửi") and user_input:
    # Gửi request tới FastAPI backend
    response = requests.post(
        "http://localhost:8000/chat",
        json={"message": user_input}
    )
    result = response.json()["response"]
    st.session_state["history"].append(("Bạn", user_input))
    st.session_state["history"].append(("Agent", result))

for who, msg in st.session_state["history"]:
    st.markdown(f"**{who}:** {msg}")