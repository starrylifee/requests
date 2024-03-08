import streamlit as st
import google.generativeai as genai

def configure_genai():
    gemini_api_key1 = st.secrets["gemini_api_key1"]
    genai.configure(api_key=gemini_api_key1)

    generation_config = {
        "temperature": 0.5,  # 소크라테스 문답법에 적합하도록 온도 조정
        "top_p": 0.85,
        "top_k": 40,
        "max_output_tokens": 100,  # 답변의 길이를 짧게 유지
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

st.title("한국 경제성장의 숨겨진 문제점 탐색 챗봇")

if 'convo' not in st.session_state:
    model = configure_genai()
    convo = model.start_chat(history=[])
    st.session_state.convo = convo
    st.session_state.chat_history = []  # 대화 기록을 저장할 리스트 초기화

user_input = st.text_input("경제성장 문제점에 대해 궁금한 점을 입력해주세요:", key="user_input")

if user_input:
    st.session_state.chat_history.append(f"**당신**: {user_input}")  # 마크다운 문법 사용
    response = st.session_state.convo.send_message(user_input)
    if response.text:
        formatted_response = f"**챗봇**: {response.text}"  # 마크다운 문법 사용
        st.session_state.chat_history.append(formatted_response)
    else:
        st.session_state.chat_history.append("**챗봇**: 답변을 받지 못했습니다. 다시 시도해주세요.")

for line in st.session_state.chat_history:  # 누적된 대화 기록을 화면에 출력, 마크다운으로 렌더링
    st.markdown(line)
