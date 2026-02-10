import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="대천명 8분 영상 자동화실", layout="centered", page_icon="🎬")

# 스타일 설정 (에러 수정 완료: unsafe_allow_html)
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; }
    .stTextArea>div>div>textarea { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 대천명 '8분+' 영상 원고 생성기")
st.info("이 시스템은 수익 창출을 위한 8분 이상의 풍성한 원고를 만드는 데 최적화되어 있습니다.")

# --- 🔑 1단계: API 키 설정 ---
with st.sidebar:
    st.header("🔑 설정")
    google_api_key = st.text_input("Google Gemini API Key", type="password")
    if google_api_key:
        genai.configure(api_key=google_api_key)

# --- 📝 2단계: 주제 입력 및 원고 생성 ---
st.header("1. 주제 및 구성 설정")
keyword = st.text_input("영상의 핵심 주제를 입력하세요", "노후에 혼자서도 외롭지 않고 당당하게 사는 법")

if st.button("8분 분량 원고 생성 시작 (클릭)"):
    if not google_api_key:
        st.error("왼쪽 사이드바에 구글 API 키를 먼저 넣어주세요!")
    else:
        with st.spinner("비서가 8분 분량(3,000자)의 대작을 집필 중입니다. 약 20~30초만 기다려주세요..."):
            
            # 분량 확보를 위한 체계적인 프롬프트
            prompt = f"""
            당신은 구독자 50만 명을 보유한 시니어 전문 유튜버이자 심리 상담가입니다.
            주제: '{keyword}'를 바탕으로 8분 이상(공백 제외 3,000자 이상)의 유튜브 나레이션 원고를 작성하세요.

            [원고 필수 구성 요소]
            1. 도입부(1분): 시청자의 외로움과 고민을 깊이 공감하고, 오늘 이야기가 왜 중요한지 강조.
            2. 본론(6분 이상): 
               - 사례 1: 깊이 있는 불교 혹은 성경 우화와 현대적 해석 (아주 상세하게)
               - 사례 2: 우리가 일상에서 흔히 겪는 구체적인 인간관계 갈등과 지혜로운 해결법
               - 사례 3: 노후의 품격을 높이는 마음가짐과 실천 방안
            3. 결론(1분): 오늘 내용을 핵심 요약하고, 시청자의 삶을 응원하는 따뜻한 메시지

            [작성 규칙]
            - 전체 글자 수는 반드시 3,000자 내외가 되어야 함.
            - 문장은 짧게 끊어서 쓰되, 성우가 읽을 때 감정을 실을 수 있도록 '...' 이나 '아려왔습니다' 같은 감성적 표현을 사용.
            - 시니어들이 듣기 편하도록 전문 용어보다는 쉬운 비유를 사용하세요.
            """
            
            try:
                # 1.5-flash-latest 모델이 가장 안정적이고 무료입니다.
                model = genai.GenerativeModel('gemini-1.5-flash-latest') 
                response = model.generate_content(prompt)
                st.session_state['final_script'] = response.text
                st.success(f"원고 생성 완료! (공백 포함 약 {len(response.text)}자 확보)")
            except Exception as e:
                st.error(f"비서가 응답하지 않습니다. 에러 내용: {e}")

# --- ✨ 3단계: 한끗 터치 및 다운로드 ---
if 'final_script' in st.session_state:
    st.markdown("---")
    st.header("2. 대천명의 '한끗 터치' (마지막 점검)")
    
    final_touch = st.text_area(
        "내용을 읽어보며 대표님의 경험이나 감정을 한두 줄 추가해 보세요.", 
        st.session_state['final_script'], 
        height=600
    )
    
    st.caption(f"현재 글자 수: 약 {len(final_touch)}자 (2,800자 이상이면 8분 영상이 가능합니다.)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 원고(.txt)로 저장하기",
            data=final_touch,
            file_name=f"{keyword}_8분원고.txt",
            mime="text/plain"
        )
    with col2:
        if st.button("📸 이미지 프롬프트 생성 (준비 중)"):
            st.info("이 원고에 어울리는 이미지 묘사를 생성합니다.")

st.markdown("---")
st.caption("대천명 '하루 30분 시스템' - 8분 영상 수익화 모델")
