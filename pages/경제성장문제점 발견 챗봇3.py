import streamlit as st
import google.generativeai as genai

def configure_genai():
    gemini_api_key1 = st.secrets["gemini_api_key1"]
    genai.configure(api_key=gemini_api_key1)

    generation_config = {
        "temperature": 0.5,  # 응답의 창의성 조절
        "top_p": 0.85,
        "top_k": 40,
        "max_output_tokens": 100,  # 응답 길이 제한
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

# 대화 내역을 표시할 컨테이너 생성
chat_container = st.container()

# 사용자 입력 받기
user_input = st.text_input("경제성장 문제점에 대해 궁금한 점을 입력해주세요:", key="user_input")

if 'convo' not in st.session_state:
    model = configure_genai()
    initial_prompt = "이 챗봇은 소크라테스 문답법을 사용하여 한국의 급격한 경제성장에 따른 문제점을 탐색하도록 도와주는 역할을 합니다. 사용자가 질문을 하면, 챗봇은 직접적인 답변 대신에 사용자로 하여금 스스로 생각하고 답을 찾을 수 있도록 가이드하는 질문을 던집니다. 이 방식으로, 사용자는 자신의 생각을 확장하고, 문제에 대한 깊이 있는 이해를 도모할 수 있습니다."
    st.session_state.convo = model.start_chat(history=[{"role": "system", "content": initial_prompt}])
    st.session_state.chat_history = []

# 사용자가 입력을 제출한 경우 처리
if user_input:
    # 챗봇으로부터 응답 받기
    response = st.session_state.convo.send_message(user_input)
    response_text = response.text if response.text else "답변을 받지 못했습니다. 다시 시도해주세요."

    # 대화 내역 업데이트
    st.session_state.chat_history.append(f"**당신**: {user_input}")
    st.session_state.chat_history.append(f"**챗봇**: {response_text}")

    # 대화 내역을 컨테이너에 표시
    with chat_container:
        for message in reversed(st.session_state.chat_history):
            st.markdown(message)
