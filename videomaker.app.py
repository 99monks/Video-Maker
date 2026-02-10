import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="대천명 AI 비서실", layout="centered", page_icon="🎬")

# 스타일 설정 (깔끔한 디자인)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🎬 대천명 5분 영상 자동화 (무료 버전)")
st.info("구글의 무료 비서(Gemini)를 사용하여 원고를 생성합니다.")

# --- 🔑 1단계: API 키 설정 ---
with st.expander("🔑 구글 비서 출근시키기 (필수 설정)", expanded=True):
    google_api_key = st.text_input("Google Gemini API Key를 입력하세요", type="password", help="AI Studio에서 발급받은 키를 넣어주세요.")
    if google_api_key:
        genai.configure(api_key=google_api_key)
        st.success("비서가 출근 준비를 마쳤습니다!")

# --- 📝 2단계: 주제 입력 및 원고 생성 ---
st.header("1. 주제 입력 및 원고 생성")
keyword = st.text_input("오늘의 영상 주제를 입력하세요", "노후에 혼자서도 당당하고 행복하게 사는 법")

if st.button("무료 비서에게 원고 맡기기"):
    if not google_api_key:
        st.error("먼저 구글 API 키를 입력해주셔야 비서를 부를 수 있습니다!")
    else:
        with st.spinner("구글 비서가 원고를 정성껏 작성 중입니다. 잠시만 기다려주세요..."):
            # 감성 프롬프트 설정
            prompt = f"""
            당신은 60대 이상 시니어들에게 ‘삶의 지혜’를 전하는 따뜻하고 공감 능력이 뛰어난 전문 작가이자 스님/목회자 같은 멘토입니다.
            주제: '{keyword}'
            
            [지시사항]
            1. 시니어들이 깊이 공감할 수 있는 감동적인 이야기나 우화를 바탕으로 작성하세요.
            2. 10분 내외 분량(공백 제외 2,500자 이상)의 아주 풍부한 나레이션 산문 형식으로 써주세요.
            3. 톤은 차분하고, 부드러우며, 시청자의 마음을 어루만지는 ‘KBS 다큐멘터리 성우’ 톤입니다.
            4. 문장은 짧고 명확하게 하되, 중간중간 감정이입을 극대화할 수 있는 묘사를 넣으세요.
               (예: "목 끝이 아려왔습니다.", "주름진 어머니의 손을 가만히 잡아보았습니다.")
            5. 마지막엔 시청자들에게 따뜻한 위로의 한마디를 건네며 마무리하세요.
            """
            
            try:
                # 1순위 모델 시도 (Flash)
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(prompt)
                st.session_state['final_script'] = response.text
                st.success("원고가 완성되었습니다!")
            except Exception as e:
                # 2순위 모델 시도 (Pro)
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    st.session_state['final_script'] = response.text
                    st.success("원고가 완성되었습니다! (기본 모델 사용)")
                except Exception as e2:
                    st.error(f"비서가 응답하지 않습니다. 에러 내용: {e2}")

# --- ✨ 3단계: 한끗 터치 및 다운로드 ---
if 'final_script' in st.session_state:
    st.markdown("---")
    st.header("2. 대천명의 '한끗 터치'")
    st.subheader("비서가 80%를 썼습니다. 이제 대표님의 영혼 20%를 채워주세요.")
    
    # 텍스트 에디터
    final_touch = st.text_area(
        "AI 원고 내용을 확인하고, 본인의 경험이나 감정 한 줄을 자유롭게 추가하세요.", 
        st.session_state['final_script'], 
        height=500
    )
    
    st.markdown("### ✅ 마무리 단계")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 원고 파일(.txt) 다운로드",
            data=final_touch,
            file_name=f"{keyword}_원고.txt",
            mime="text/plain"
        )
    with col2:
        if st.button("✨ 썸네일 문구 추천받기"):
            st.warning(f"추천: '{keyword}' - 이 한 줄만으로 인생이 달라집니다.")

st.markdown("---")
st.caption("대천명의 '하루 30분 시스템' | Powered by Google Gemini Free Tier")
