import streamlit as st
import requests

AGENT_API_URL = "http://localhost:8001/agent/run"

st.set_page_config(page_title="AI Support Agent", layout="centered")

st.title("AI Support Agent")
st.caption("Sentiment Tool + Agent + Groq LLM")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call agent API
    try:
        response = requests.post(
            AGENT_API_URL,
            json={
                "user_id": "demo_user",
                "message": prompt
            },
            timeout=10
        ).json()

        # Debug: Print the full response
        st.write("DEBUG - Full API Response:")
        st.json(response)

        # Check if response has the expected keys
        if 'action' in response and 'sentiment' in response and 'next_message' in response:
            agent_reply = f"""
**Action:** {response['action']}

**Sentiment:** {response['sentiment']}  
**Confidence:** {response['confidence_score']}%

**Agent Reply:**  
{response['next_message']}

**Reasoning:**  
_{response['reasoning']}_
"""

            st.session_state.messages.append({"role": "assistant", "content": agent_reply})

            with st.chat_message("assistant"):
                st.markdown(agent_reply)
        else:
            st.error(f"Unexpected response format. Response keys: {response.keys()}")

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
