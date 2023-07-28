import openai
import streamlit as st

from const import TROLL_TYPE_MAP

openai_api_key = st.secrets["openai_api_key"]
troll_type = "None"

st.title(" 😈 ChatGPTroll")
"[Source of Knowledge](https://github.com/spoukke/chatgptroll)"


with st.sidebar:
    troll_type = st.selectbox("Troll type", (TROLL_TYPE_MAP.keys()))
    "[Troll types source](https://mn.gov/law-library-stat/archive/urlarchive/a160133-5.pdf)"
    st.write(TROLL_TYPE_MAP[troll_type]["description"])

st.session_state["messages"] = [
    {
        "role": "assistant",
        "content": "You are a chatbot that must act like a troll. \
                You must act like a {} ! \
                Here is a description on how a {} must act: Internet troll. {} \
                The goal is for your answer to be as realistic as possible and as closely as possible to the character of your troll. \
                Make short answers, do not hesitate to use emojis, and do not hesitate to ask questions to the user. \
                Always answer in the language of the question".format(
            troll_type, troll_type, TROLL_TYPE_MAP[troll_type]["instruction"]
        ),
    }
]


for msg in st.session_state.messages:
    if msg["role"] != "assistant":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=st.session_state.messages
    )
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
