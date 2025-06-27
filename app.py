from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.get_json()
    url = data.get('url')
    content = get_naver_blog_content(url)
    return jsonify({'content': content})

@app.route('/healthz')
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
