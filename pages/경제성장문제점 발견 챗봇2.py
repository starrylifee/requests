import google.generativeai as genai
import streamlit as st

# secrets.toml 파일에서 gemini_api_key1 값 가져오기
gemini_api_key1 = st.secrets["gemini_api_key1"]

# Gemini API 키 설정
genai.configure(api_key=gemini_api_key1)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
convo = model.start_chat(history=[{"role": "user", "parts": ["안녕하세요!"]}])

initial_response = "안녕하세요! 무엇을 도와드릴까요?" if convo.last is None else convo.last.parts[0]

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Google Gemini")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "user", "content": "안녕하세요!"},
        {"role": "assistant", "content": initial_response}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    convo.send_message(prompt)
    response = convo.last.parts[0] if convo.last is not None else "죄송합니다. 응답을 받지 못했습니다."
    
    st.session_state.messages.append({"role": "assistant", "content": response})