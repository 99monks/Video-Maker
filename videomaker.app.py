import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="대천명 8분 영상 자동화실", layout="centered", page_icon="🎬")

# 스타일 설정
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; }
    .stTextArea>div>div>textarea { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 대천명 '8분+' 영상 원고 생성기")
st.info("구글 무료 비서 모델을 최적화하여 연결합니다.")

# --- 🔑 1단계: API 키 설정 ---
with st.sidebar:
    st.header("🔑 설정")
    google_api_key = st.text_input("Google Gemini API Key", type="password")
    if google_api_key:
        genai.configure(api_key=google_api_key)

# --- 📝 2단계: 주제 입력 및 원고 생성 ---
st.header("1. 주제 및 구성 설정")
keyword = st.text_input("영상의 핵심 주제를 입력하세요", "나이 들수록 입은 닫고 주머니는 열어야 대접받는 진짜 이유")

if st.button("8분 분량 원고 생성 시작 (클릭)"):
    if not google_api_key:
        st.error("왼쪽 사이드바에 구글 API 키를 먼저 넣어주세요!")
    else:
        with st.spinner("비서가 원고를 작성 중입니다. 약 30초만 기다려주세요..."):
            
            prompt = f"""
            당신은 시니어 전문 유튜버이자 작가입니다. 
            주제: '{keyword}'를 바탕으로 8분 이상(3,000자 이상)의 유튜브 원고를 작성하세요.
            [도입-본론(사례3개)-결론] 구조로 아주 상세하고 따뜻하게 써주세요.
            """
            
            # 🚀 모델 연결 에러를 방지하기 위한 3단계 시도
            success = False
            # 시도할 모델 리스트 (가장 확실한 순서대로)
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(prompt)
                    st.session_state['final_script'] = response.text
                    st.success(f"성공! 사용된 비서 모델: {m_name}")
                    success = True
                    break # 성공하면 반복문 탈출
                except Exception as e:
                    continue # 에러 나면 다음 모델로 시도
            
            if not success:
                st.error("모든 무료 모델이 응답하지 않습니다. API 키가 활성화되었는지, 혹은 할당량이 초과되지 않았는지 확인해주세요.")

# --- ✨ 3단계: 한끗 터치 및 다운로드 ---
if 'final_script' in st.session_state:
    st.markdown("---")
    st.header("2. 대천명의 '한끗 터치'")
    final_touch = st.text_area("내용 수정 및 글자 수 확인", st.session_state['final_script'], height=600)
    st.caption(f"현재 글자 수: 약 {len(final_touch)}자")
    
    st.download_button(
        label="📄 원고(.txt)로 저장하기",
        data=final_touch,
        file_name=f"대천명_원고.txt",
        mime="text/plain"
    )
