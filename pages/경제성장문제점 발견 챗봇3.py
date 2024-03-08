# 필요한 라이브러리를 불러옵니다.
import streamlit as st
import google.generativeai as genai
import toml

# Google GenerativeAI 및 Gemini 모델 설정
def configure_genai():

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
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

# 스트림릿 UI 설정
st.title("한국 경제성장의 숨겨진 문제점 탐색")

# 사용자 입력을 세션 상태에 저장하기 위한 초기화
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# 대화 이력을 저장하기 위한 세션 상태 초기화
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# 사용자 입력
user_input = st.text_input("한국의 경제성장에 대해 궁금한 점을 입력해주세요:", key="user_input")

if st.button('질문하기') or st.session_state.user_input:
    # API 설정 및 모델 초기화
    model = configure_genai()

    # 챗봇 대화 시작
    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["반드시 지켜야 할 것 - 질문을 할 때 질문의 답과 대한 힌트를 주지 마세요. 예를 들어주지 마세요. 학생에게 도움이 안됩니다.안녕! 오늘은 한국의 경제성장에 따른 여러 문제점에 대해 함께 탐색해 볼 거야. 너 스스로 생각하고 발견하는 과정을 통해, 경제성장의 이면에 숨겨진 다양한 문제들을 이해하고, 어떻게 해결할 수 있을지 고민해 보자. 시작해 볼까?첫 번째 질문: \"경제성장이란 무엇일까요? 그리고 이것이 우리 일상에 어떤 긍정적인 영향을 줄 수 있을까요?\"이 질문을 통해 경제성장의 기본 개념과 긍정적인 측면에 대해 생각해 보도록 해.두 번째 질문: \"하지만, 경제가 빠르게 성장하면서 생길 수 있는 문제는 무엇이라고 생각하나요?\"세 번째 질문:  그 문제에 대해 좀 더 자세히 이야기해줘.네 번째 질문:  맞아 네가 말한 내용은 경제성장에 대한 문제점이야. 요약하면 다음과 같아.이러한 질문들을 통해, 너는 한국의 경제성장 과정에서 발생할 수 있는 다양한 문제들을 스스로 발견할 수 있을거야!"]
        },
        {
            "role": "model",
            "parts": ["안녕! 오늘은 한국의 경제성장에 따른 여러 문제점에 대해 함께 탐색해 볼 거야. 너 스스로 생각하고 발견하는 과정을 통해, 경제성장의 이면에 숨겨진 다양한 문제들을 이해하고, 어떻게 해결할 수 있을지 고민해 보자. 시작해 볼까? 첫 번째 질문: \"경제성장이란 무엇일까요? 그리고 이것이 우리 일상에 어떤 긍정적인 영향을 줄 수 있을까요?\""]
        },
        {
            "role": "user",
            "parts": ["돈을 많이 벌고 인구가 늘고 부동산이 늘어나는 것"]
        },
        {
            "role": "model",
            "parts": ["맞아요. 경제성장은 일반적으로 국민소득이나 생산량의 증가로 측정되며, 이는 돈을 많이 벌고, 인구가 늘고, 부동산이 늘어나는 것과 같은 여러 긍정적인 영향을 미칠 수 있습니다. 하지만 경제성장이 빠른 속도로 진행될 때 발생할 수 있는 잠재적인 문제점에 대해서도 생각해 볼 필요가 있어요. 이제 두 번째 질문으로 넘어가 볼까요? \"하지만, 경제가 빠르게 성장하면서 생길 수 있는 문제는 무엇이라고 생각하나요?\""]
        },
        {
            "role": "user",
            "parts": ["환경오염이 될 것 같아"]
        },
        {
            "role": "model",
            "parts": ["맞아요. 환경오염은 경제성장이 빠른 속도로 진행될 때 발생할 수 있는 잠재적인 문제점 중 하나입니다. 경제활동이 증가하면 에너지 소비와 자원 사용량이 증가하여 공기, 물, 토양 오염으로 이어질 수 있습니다. 이러한 환경오염은 인간의 건강과 생태계에 부정적인 영향을 미칠 수 있습니다. 이제 세 번째 질문으로 넘어가 볼까요? \"그 문제에 대해 좀 더 자세히 이야기해줘.\""]
        },
        {
            "role": "user",
            "parts": ["환경이 많이 더러워지고 쓰레기 버리는 것에 문제가 생길것 같아"]
        },
        {
            "role": "model",
            "parts": ["네, 말씀하신 내용은 경제성장이 환경에 미칠 수 있는 문제점에 대한 구체적인 예입니다. 경제활동이 증가하면 쓰레기와 오염물질의 양도 증가합니다. 이로 인해 쓰레기 매립지가 가득 차고, 수자원이 오염되며, 대기 질이 저하될 수 있습니다. 또한, 빠른 경제성장은 자원 고갈로 이어질 수 있으며, 이는 환경에 추가적인 부담을 줄 수 있습니다. 이러한 문제를 해결하려면 지속 가능한 관행, 폐기물 관리 개선, 청정 에너지원으로의 전환과 같은 조치가 필요할 수 있습니다."]
        },
        {
            "role": "user",
            "parts": ["마지막에 또 어떤 문제가 있을까요? 하며 확산적인 질문을 해줘. 예시를 제시하지 말고, 학생이 스스로 생각할 수 있도록"]
        },
        {
            "role": "model",
            "parts": ["경제성장의 잠재적인 문제점에 대해 지금까지 논의한 것 외에도 생각해 볼 수 있는 또 다른 문제가 있을까요? 이 문제는 환경적, 사회적, 경제적 영향을 미칠 수 있습니다. 경제성장이 너무 빠르게 진행되거나 적절하게 관리되지 않을 때 발생할 수 있는 문제점에 대해 창의적으로 생각해 보세요."]

        },
    ])
    
    # 사용자 입력과 모델 응답을 대화 이력에 추가
    st.session_state.conversation_history.append(f"User: {st.session_state.user_input}")

    # 사용자의 입력을 모델에 전송하고 응답 받기
    convo.send_message(user_input)
    response = convo.last.text

    # 모델의 응답을 대화 이력에 추가
    st.session_state.conversation_history.append(response)

    # 입력 필드 초기화
    st.session_state.user_input = ""
    #대화 이력을 마크다운으로 보기 좋게 표시
    if st.session_state.conversation_history:
        conversation_markdown = "\n\n".join(st.session_state.conversation_history)
        st.markdown(conversation_markdown)