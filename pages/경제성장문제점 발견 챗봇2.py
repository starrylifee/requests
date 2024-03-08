from openai import OpenAI
import streamlit as st
import time

# 업데이트된 Assistant ID
assistant_id = "asst_ZSXICkAPTIg5ZsEFJxWmkJmj"
client = OpenAI(api_key=st.secrets["api_key1"])

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password1"]

# 입력된 비밀번호가 정확한지 확인
if password != correct_password:
    st.error("비밀번호가 틀렸습니다. 올바른 비밀번호를 입력해주세요.")
    st.stop()

with st.sidebar:
    # 스레드 ID 관리
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = ""

    thread_btn = st.button("Create a new thread")

    if thread_btn:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id  # 스레드 ID를 session_state에 저장
        st.subheader(f"Created Thread ID: {st.session_state.thread_id}")
        st.info("스레드가 생성되었습니다.")
        st.info("스레드 ID를 기억하면 대화내용을 이어갈 수 있습니다.")
        st.divider()
        st.subheader("추천 질문")
        st.info("OOOO문제가 있어.")

# 스레드 ID 입력란을 자동으로 업데이트
thread_id = st.text_input("Thread ID", value=st.session_state.thread_id)

st.title("법률제작 보조 챗봇")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 저는 경제발전의 문제점을 찾는 것을 도와주는 봇입니다. 어떻게 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not thread_id:
        st.error("Please add your thread_id to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)

    msg = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
