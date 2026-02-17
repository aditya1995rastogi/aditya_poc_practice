import streamlit as st
import requests
import os

os.environ["DATABRICKS_TOKEN"] = dbutils.secrets.get(scope="project-dev", key="databricks-token")

st.set_page_config(page_title="Drug Info AI Assistant")

st.title("Drug Info AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about a drug...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://dbc-41fdb423-e2e5.cloud.databricks.com/serving-endpoints/drug_chatbot/invocations"

    headers = {
        "Authorization": f"Bearer {os.environ['DATABRICKS_TOKEN']}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    else:
        answer = response.text

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
