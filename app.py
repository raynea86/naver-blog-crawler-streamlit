import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_naver_blog_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    iframe = soup.find("iframe", {"id": "mainFrame"})
    if not iframe:
        return "iframe(mainFrame) not found"
    iframe_url = "https://blog.naver.com" + iframe["src"]
    res2 = requests.get(iframe_url, headers=headers)
    soup2 = BeautifulSoup(res2.text, "html.parser")
    main = soup2.find("div", {"class": "se-main-container"})
    if not main:
        main = soup2.find("div", {"id": "postViewArea"})
    if not main:
        return "본문 영역을 찾지 못했습니다."
    return main.get_text(strip=True)

st.title("네이버 블로그 본문 추출기 (Streamlit)")

url = st.text_input("네이버 블로그 글 URL을 입력하세요", placeholder="https://blog.naver.com/yourid/123456789")

if st.button("본문 추출"):
    if url:
        with st.spinner("본문을 가져오는 중입니다..."):
            content = get_naver_blog_content(url)
        st.text_area("본문 결과", value=content, height=400)
    else:
        st.warning("URL을 입력하세요.")
