import streamlit as st
from google import genai

# ==========================================
# 🔑 내 정보 입력하기
# ==========================================
GEMINI_API_KEY = "AIzaSyASGViFJE3YvY26Sb2iIveTCAJqUl3Lxes"
# ==========================================

# 📱 1. 웹 앱의 기본 디자인 설정 (웹 브라우저 탭 이름, 아이콘)
st.set_page_config(page_title="나만의 주식 비서", page_icon="📈", layout="centered")

# 📱 2. 화면에 보일 제목과 설명 쓰기
st.title("📈 나만의 AI 주식 비서")
st.write("버튼을 누르면 AI가 실시간 뉴스를 분석해 오늘의 리포트를 가져옵니다!")

# 🧠 3. AI 분석 기능 (이전과 똑같습니다)
def get_stock_report():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    너는 전문 주식 애널리스트야. 반드시 구글 검색을 사용하여 오늘 날짜의 가장 최신 뉴스 및 주식 시장(미장/국장 상승·하락 여부) 실제 팩트를 확인한 후 아래 항목을 작성해. 사실과 다른 내용을 지어내면 절대 안 돼. 모든항목은 무조건 사실기반으로 정확한 수치기반으로 작성해줘.
    
    [중요 규칙]
    - 웹사이트에 예쁘게 보여줄 거니까, 제목에는 ## 기호를 쓰고 목록에는 - 기호를 써서 '마크다운' 형식으로 깔끔하게 꾸며줘.
    - 텔레그램에서 쓰던 '|||' 가위표 기호는 이제 절대 쓰지 마! (웹에서는 자를 필요가 없어)
    
    1. 🌍 최신 세계적 이슈와 미장/국장 요약 (반드시 검색된 팩트 기반)
    2. 🇰🇷 금일 국장 핫이슈 예상
    3. 🔥 당일 핫 섹터 TOP 3 (우선순위 별)
    4. 🎯 섹터별 대장종목 (최대 3개) 및 각 항목별 구체적인 추천 이유
    """
    
    response = client.models.generate_content(
            model='models/gemini-2.5-flash', 
            contents=prompt,
            config={'tools': [{'google_search': {}}]} 
        )
    return response.text

# 📱 4. 화면에 '분석 시작' 버튼 만들기
st.divider()

if st.button("🔄 최신 리포트 분석하기", type="primary"):
    with st.spinner('🧠 AI가 실시간 정보를 분석 중입니다...'):
        try:
            report = get_stock_report()
            st.success("✅ 분석 완료!")
            st.markdown(report)
        except Exception as e:
            st.error(f"🚨 에러가 발생했습니다: {e}")
            st.info("💡 팁: 구글 API 무료 사용량(하루 20~50회)을 초과했거나 모델 이름이 변경되었을 수 있습니다.")
