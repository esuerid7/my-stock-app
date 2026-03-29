import streamlit as st
import random
from google import genai

# ==========================================
# 🔑 내 정보 입력하기
# ==========================================
GEMINI_API_KEY = "AIzaSyASGViFJE3YvY26Sb2iIveTCAJqUl3Lxes"
# ==========================================

st.set_page_config(page_title="GTO 홀덤 마스터", page_icon="♠️")

st.title("♠️ GTO 오픈 레인지 트레이너")
st.write("토너먼트 상황에서 올바른 결정을 내리는 연습을 하세요.")

# 1. 문제 생성 데이터
positions = ["UTG", "MP", "CO", "BTN", "SB"]
stack_sizes = ["15BB (숏스택)", "30BB (미들스택)", "50BB+ (딥스택)"]
card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
card_suits = ["s (Sutied)", "o (Off-suit)"]

# 2. 세션 상태 초기화 (문제를 유지하기 위함)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None

def generate_quiz():
    pos = random.choice(positions)
    stack = random.choice(stack_sizes)
    # 랜덤 카드 생성 (예: AKs, 78o, 22)
    c1 = random.choice(card_ranks)
    c2 = random.choice(card_ranks)
    
    # 높은 카드를 앞으로
    r1, r2 = (c1, c2) if card_ranks.index(c1) >= card_ranks.index(c2) else (c2, c1)
    
    if r1 == r2:
        hand = f"{r1}{r2}" # 포켓 페어
    else:
        hand = f"{r1}{r2}{random.choice(['s', 'o'])}"
        
    st.session_state.quiz_data = {"pos": pos, "stack": stack, "hand": hand}

# 3. 화면 구성
if st.button("🎰 새로운 문제 생성"):
    generate_quiz()

if st.session_state.quiz_data:
    q = st.session_state.quiz_data
    st.info(f"**상황:** {q['pos']} 포지션 / 스택: {q['stack']}")
    st.subheader(f"내 핸드: 🎴 {q['hand']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 오픈 (Raise)"):
            st.session_state.user_choice = "Open"
    with col2:
        if st.button("❌ 폴드 (Fold)"):
            st.session_state.user_choice = "Fold"

    # 4. AI 정답 확인
    if 'user_choice' in st.session_state:
        st.divider()
        with st.spinner('🧐 AI가 GTO 관점에서 분석 중...'):
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            prompt = f"""
            너는 GTO 홀덤 전문가야. 아래 토너먼트 상황에서 해당 핸드가 '표준적인 GTO 오픈 레인지'에 포함되는지 판단해줘.
            - 상황: {q['pos']}, {q['stack']}
            - 핸드: {q['hand']}
            - 유저의 선택: {st.session_state.user_choice}

            작성 형식:
            1. 결론: (유저의 선택이 GTO상 맞는지 틀린지)
            2. 이론적 근거: (해당 포지션에서 이 핸드의 가치 설명)
            3. 전략 팁: (비슷한 상황에서 고려할 점)
            """
            
            try:
                # 404 에러 방지를 위해 가장 확실한 모델명 사용
                response = client.models.generate_content(
                    model='gemini-1.5-flash', 
                    contents=prompt
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류 발생: {e}")
        
        # 선택 초기화
        del st.session_state.user_choice
