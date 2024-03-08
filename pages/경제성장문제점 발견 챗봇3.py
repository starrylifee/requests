import streamlit as st
import google.generativeai as genai

def configure_genai():
    gemini_api_key1 = st.secrets["gemini_api_key1"]
    genai.configure(api_key=gemini_api_key1)

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

st.title("한국 경제성장의 숨겨진 문제점 탐색")

if 'convo' not in st.session_state:
    model = configure_genai()
    convo = model.start_chat(history=[
        {"role": "system", "parts": ["한국의 경제성장 과정에서 발생할 수 있는 문제점에 대해 토론해봅시다. 대화상태를 어린이로 한정하여 화법을 사용하고, 문제점을 어린이 스스로 생각할 수 있도록 예를 들지 않고 소크라테스 문답법을 활용하여 학생 스스로 유추하도록 해줘. 학생이 바르게 유추하면 칭찬해줘"]}
    ])
    st.session_state.convo = convo


user_input = st.text_input("경제성장 문제점에 대해 궁금한 점을 입력해주세요:", key="user_input")

if st.button('질문하기') or st.session_state.user_input:
    convo = st.session_state.convo

    if st.session_state.user_input:
        convo.extend_conversation([{"role": "user", "parts": [st.session_state.user_input]}])
    else:
        st.error("텍스트를 입력해주세요.")

    convo.extend_conversation([{"role": "user", "parts": [st.session_state.user_input]}])
    response = convo.last.text
    st.session_state.user_input = ""
    st.markdown(response)