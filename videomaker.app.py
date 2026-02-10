import streamlit as st
import openai
import anthropic

st.set_page_config(page_title="대천명 AI 비서실", layout="centered")

st.title("🎬 대천명 5분 영상 자동화 시스템")
st.markdown("---")

# 🔑 API 키 입력 (한 번만 입력하면 됩니다)
with st.expander("🔑 비서들 출근시키기 (API Key 설정)"):
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    anthropic_api_key = st.text_input("Claude API Key", type="password")

# 1️⃣ [Step 1] 기획 비서 (ChatGPT)
st.header("1. 기획 비서 (아이디어)")
keyword = st.text_input("주제 키워드를 입력하세요", "노후 인간관계")

if st.button("기획 비서 소환"):
    if not openai_api_key:
        st.error("OpenAI API 키를 입력해주세요.")
    else:
        client = openai.OpenAI(api_key=openai_api_key)
        prompt = f"60대 이상 시니어들에게 ‘삶의 지혜’를 전하는 스토리텔러로서, '{keyword}' 주제의 감동적인 이야기 줄거리 1가지를 요약해줘."
        with st.spinner("기획 중..."):
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            st.session_state['idea'] = res.choices[0].message.content
            st.success("기획 완료!")

if 'idea' in st.session_state:
    st.info(st.session_state['idea'])

    # 2️⃣ [Step 2] 작가 비서 (Claude)
    st.header("2. 작가 비서 (원고 작성)")
    if st.button("작가 비서 소환"):
        if not anthropic_api_key:
            st.error("Claude API 키를 입력해주세요.")
        else:
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            prompt = f"당신은 시니어 전문 스크립트 작가입니다. 다음 줄거리를 바탕으로 10분 분량(2000자 이상)의 나레이션 산문 원고를 작성하세요: {st.session_state['idea']}"
            with st.spinner("원고 집필 중..."):
                res = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.session_state['script'] = res.content[0].text

if 'script' in st.session_state:
    # 3️⃣ [Step 3] 한끗 터치 (영혼 불어넣기)
    st.header("3. 한끗 터치 (대표님 전용)")
    final_script = st.text_area("AI가 쓴 원고입니다. 여기서 대표님의 경험을 한 줄 추가하세요.", st.session_state['script'], height=400)
    
    # 4️⃣ [Step 4] Vrew 전송용 복사
    st.success("이제 아래 원고를 복사해서 Vrew에 붙여넣으세요!")
    st.download_button("원고 다운로드 (.txt)", final_script)

st.markdown("---")
st.caption("대천명의 '하루 30분 시스템' 자동화 도구")