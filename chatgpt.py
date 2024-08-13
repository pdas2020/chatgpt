from openai import OpenAI
import streamlit as st
import time

col1, col2, col3 = st.columns([4,4,4])

col1.markdown("# This is my GPT")
col1.markdown(" This is MVP")

uploaded_photo = col2.file_uploader("Upload a photo" )
camera_photo = col2.camera_input("Take a photo" )

progress_bar = col2.progress(0)

for percent_complete in range(100):
        time.sleep(0.05)
        progress_bar.progress(percent_complete+1)

col2.success("Photo sucessfully uploaded")

with st.expander("Click here"):
        st.write ("Hello, How are you doing?")

        if uploaded_photo is None:
            st.image(camera_photo)
        else:
            st.image(uploaded_photo) 


st.title("FinanceGPT-Ask me Anything")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

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