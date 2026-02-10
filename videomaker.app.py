import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="대천명 무료 AI 비서실", layout="centered")

st.title("🎬 대천명 5분 영상 자동화 (무료 버전)")
st.markdown("---")

# 🔑 구글 제미나이 API 키 입력
with st.expander("🔑 구글 비서 출근시키기 (API Key 설정)"):
    google_api_key = st.text_input("Google Gemini API Key를 입력하세요", type="password")
    if google_api_key:
        genai.configure(api_key=google_api_key)

# 1️⃣ [Step 1] 기획 및 원고 작성 통합 (무료니까 한 번에!)
st.header("1. 주제 입력 및 원고 생성")
keyword = st.text_input("오늘의 영상 주제", "노후에 혼자서도 행복하게 사는 법")

if st.button("무료 비서에게 원고 맡기기"):
    if not google_api_key:
        st.error("구글 API 키를 먼저 입력해주세요!")
    else:
        model = genai.GenerativeModel('gemini-1.5-flash') # 무료이면서 빠른 모델
        
        # 대표님의 황금 프롬프트 통합본
        prompt = f"""
        당신은 60대 이상 시니어들에게 ‘삶의 지혜’를 전하는 따뜻한 스토리텔러이자 전문 작가입니다.
        주제: '{keyword}'
        
        [지시사항]
        1. 시니어들이 깊이 공감할 수 있는 감동적인 이야기나 불교/성경 우화를 바탕으로 작성하세요.
        2. 10분 분량(공백 제외 2,000자 이상)의 나레이션 산문 형식으로 써주세요.
        3. 톤은 차분하고 깊은 공감을 주는 다큐 성우 톤이어야 합니다.
        4. 중간에 "목 끝이 아려왔습니다", "주름진 손을 보며" 같은 감성적인 묘사를 넣어주세요.
        """
        
        with st.spinner("구글 비서가 열심히 원고를 쓰는 중..."):
            try:
                response = model.generate_content(prompt)
                st.session_state['final_script'] = response.text
                st.success("원고가 완성되었습니다!")
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

if 'final_script' in st.session_state:
    # 2️⃣ [Step 2] 한끗 터치 (영혼 불어넣기)
    st.header("2. 한끗 터치 (대표님의 영혼)")
    user_touch = st.text_area("AI 원고에 대표님의 경험을 한 줄 더해주세요.", st.session_state['final_script'], height=400)
    
    # 3️⃣ [Step 3] Vrew용 다운로드
    st.download_button("최종 원고 다운로드 (.txt)", user_touch)
    st.info("이 원고를 복사해서 Vrew에 넣으시면 영상 제작 끝!")

st.markdown("---")
st.caption("대천명의 '하루 30분 시스템' (Powered by Google Gemini)")
