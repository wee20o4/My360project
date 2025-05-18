from flask import Flask, request, render_template # type: ignore
import requests
import os

app = Flask(__name__)

API_KEY = 'AIzaSyBDugCCbNE04W77vDE8IeCgM4ZFw6KQTjw'  # <-- Thay bằng key thật của bạn
API_URL = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={API_KEY}'



@app.route("/", methods=["GET"])
def index():
    return render_template("api.html")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.form.get("prompt")

    if not prompt:
        return render_template("api.html", response="Vui lòng nhập nội dung.")

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        return render_template("api.html", response=f"Lỗi API: {response.status_code} - {response.text}")

    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        text = "Không có phản hồi hợp lệ từ API."

    return render_template("api.html", response=text)


if __name__ == "__main__":
    app.run(debug=True)
