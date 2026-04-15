from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "백엔드 서버 연결 성공!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
