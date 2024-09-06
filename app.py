from openai import OpenAI
import streamlit as st
import os

st.title("AIBot-Ask me Anything")

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

#initialize session variable at the start
st.sidebar.title =("Model Parameters")
temperature = st.sidebar.slider("Temperature",min_value=0.0, max_value=2.0,value=0.7,step=0.1 )
max_token = st.sidebar.slider("Max Token",min_value=1, max_value=1000,value=256 )    

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})