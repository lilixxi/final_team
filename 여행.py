import streamlit as st
import base64

# 이미지를 base64 문자열로 변환하는 함수
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 기본 배경 이미지 설정 함수
def basic_background(png_file, opacity=1):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        width: 100%;
        height: 100vh;
        opacity: {opacity};
        z-index: 0;
        position: fixed; 
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

background_image = '사진/2페이지 배경.png'  # 메인 페이지 배경 이미지 설정
basic_background(background_image)

# 페이지 설정
def main_page():
    background_image = '사진/배경 수정3.png'  # 메인 페이지 배경 이미지 설정
    basic_background(background_image)
    
    st.title("메인 페이지")
    st.write("여기는 메인 페이지입니다.")
    
    # CSS로 버튼 위치 조정
    st.markdown("""
        <style>
        div.stButton > button {
            position: fixed;
            bottom: 20px;  /* 화면 하단에서 20px 위 */
            left: 50%;     /* 화면 왼쪽에서 50% 위치 */
            transform: translateX(-50%);  /* 가로 축 기준 중앙 정렬 */
            background-color: #4CAF50; /* 초록색 배경 */
            color: white;
            padding: 15px 32px;
            font-size: 16px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # 버튼 클릭 시 페이지 전환
    if st.button("효자SON 이용하기 ▶️"):
        st.session_state.page = "second"

def second_page():
    st.title("두 번째 페이지")
    st.write("여기는 두 번째 페이지입니다.")
    st.write("여기에 다른 내용을 추가할 수 있습니다.")
    st.set_page_config(page_title="건강검진 챗봇", layout="wide")
    st.title("건강검진 챗봇")
    st.write("질문을 입력하세요:")

    query = st.text_input("질문:")

    chat_history = []

    if query:
        response = process_query(query)
        chat_history.append({"user": query, "bot": response})

    if chat_history:
        for chat in chat_history:
            st.write(f"**사용자:** {chat['user']}")
            st.write(f"**챗봇:** {chat['bot']}")
            st.write("---")
    
    # CSS로 버튼 위치 조정
    st.markdown("""
        <style>
        div.stButton > button {
            position: fixed;
            bottom: 20px;  /* 화면 하단에서 20px 위 */
            left: 50%;     /* 화면 왼쪽에서 50% 위치 */
            transform: translateX(-50%);  /* 가로 축 기준 중앙 정렬 */
            background-color: #4CAF50; /* 초록색 배경 */
            color: white;
            padding: 15px 32px;
            font-size: 16px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("메인 페이지로 돌아가기"):
        st.session_state.page = "main"

# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "main"

# 페이지 전환
if st.session_state.page == "main":
    main_page()
else:
    second_page()
