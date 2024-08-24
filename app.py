import streamlit as st
from PIL import Image
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAI
from utils import QdrantRetriever, ensemble_search, generate_gpt4_response  # 여기서 utils로 부터 가져옴
import time


# 메인 화면 설정
st.set_page_config(page_title="효자손 챗봇 서비스", layout="wide")

# 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "메인"

# 메인 페이지
if st.session_state.page == "메인":
    # 메인 화면 이미지 불러오기
    image = Image.open('효자손.png')
    st.image(image, use_column_width=True)

    # 시작하기 버튼
    if st.button("시작하기"):
        st.session_state.page = "챗봇"
        st.experimental_rerun()

# 챗봇 페이지
if st.session_state.page == "챗봇":
    # OpenAI API 키 설정
    openai_api_key = "YOUR_OPENAI_API_KEY"
    QDRANT_URL = ""
    QDRANT_API_KEY = ""
    COLLECTION_NAME = "son99_d"

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    st_model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    openai_client = OpenAI(api_key=openai_api_key)

    st.title("효자손 챗봇")

    # 사용자 입력
    user_query = st.text_input("질문을 입력하세요:")

    if user_query:
        with st.spinner("챗봇이 답변을 작성 중입니다..."):
            # 쿼리 처리 후 응답 생성
            final_results = ensemble_search(user_query, client, COLLECTION_NAME)
            if final_results:
                response = final_results[0].page_content
            else:
                response = "관련된 답변을 찾을 수 없습니다. 다른 질문을 해보세요."
            time.sleep(2)  # 로딩 시간을 실제로 더 느리게 보이게 하려면 제거 가능

            # 챗봇 형식으로 출력
            st.write(f"**사용자**: {user_query}")
            st.write(f"**챗봇**: {response}")
