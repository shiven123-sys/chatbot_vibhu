import streamlit as st
import cohere
import socket

# ⚠️ Direct API Key (for local testing only)
COHERE_API_KEY = "Wo05N7rZgMBWDIR7IG8IwilNmLoJVG6MF9JQlZWl"

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

st.set_page_config(page_title="Cohere Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 vibhu")
st.write("Chatbot using Cohere API (with Offline fallback)")

# Session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Show chat history
for role, content in st.session_state["messages"]:
    if role == "User":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Bot:** {content}")

# Simple offline fallback function
def offline_reply(message: str) -> str:
    msg = message.lower()
    if "hello" in msg or "hi" in msg:
        return "👋 Hi! (offline mode)"
    elif "bye" in msg:
        return "👋 Goodbye! (offline mode)"
    elif "name" in msg:
        return "I am a local backup bot (offline mode)."
    else:
        return "🤖 Sorry, I'm offline now. Please check your internet."

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append(("User", user_input))

    try:
        # First try online Cohere
        response = co.chat(
            model="command-r-plus",   # ✅ new model (not deprecated)
            message=user_input,
            chat_history=[
                {"role": role, "message": msg}
                for role, msg in st.session_state["messages"]
                if role in ["User", "Chatbot"]
            ]
        )

        reply = response.text
        st.session_state["messages"].append(("Chatbot", reply))

    except (socket.gaierror, Exception) as e:
        # If network error, use offline fallback
        st.warning("⚠️ Network issue detected, switching to offline mode.")
        reply = offline_reply(user_input)
        st.session_state["messages"].append(("Chatbot", reply))

