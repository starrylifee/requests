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

    model = genai.GenerativeModel(model_name="gemini-pro",  # 모델 이름 확인 필요, 예시로 'gemini-pro' 사용
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

st.title("한국 경제성장의 숨겨진 문제점 탐색")

if 'convo' not in st.session_state:
    model = configure_genai()
    convo = model.start_chat(history=[])  # 초기 대화 상태 설정, 'system' 메시지 제거
    st.session_state.convo = convo
    st.session_state.chat_history = []  # 대화 기록을 저장할 리스트 초기화

user_input = st.text_input("경제성장 문제점에 대해 궁금한 점을 입력해주세요:", key="user_input")

if user_input:  # 사용자 입력 처리
    st.session_state.chat_history.append(f"당신: {user_input}")  # 사용자 입력을 대화 기록에 추가
    response = st.session_state.convo.send_message(user_input)  # 수정된 메서드 사용
    response_text = response.text if response.text else "답변을 받지 못했습니다. 다시 시도해주세요."
    st.session_state.chat_history.append(f"챗봇: {response_text}")  # 챗봇의 응답을 대화 기록에 추가

for line in st.session_state.chat_history:  # 누적된 대화 기록을 화면에 출력
    st.text(line)
