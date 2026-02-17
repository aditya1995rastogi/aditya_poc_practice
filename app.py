import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError
import requests
import os


# Initialize Databricks client (uses app service identity automatically)
w = WorkspaceClient()

ENDPOINT_NAME = "drug_chatbot"

st.set_page_config(page_title="Drug Info AI Assistant", layout="wide")
st.title("Drug Info AI Assistant")

# Store conversation in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask about a drug...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        token = w.secrets.get_secret(scope="project-dev", key="databricks-token").value
        host = w.config.host.rstrip("/")

        response = requests.post(
        f"{host}/serving-endpoints/{ENDPOINT_NAME}/invocations",
        headers={"Authorization": f"Bearer {token}"},
        json={"inputs": {"query": prompt}}
        )
        response.raise_for_status()
        answer = response.json()["predictions"]["result"]

    except DatabricksError as e:
        answer = f"Databricks error: {str(e)}"

    except Exception as e:
        answer = f"Unexpected error: {str(e)}"

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)