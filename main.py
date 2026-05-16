from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 투두 입력 데이터 형식
class WeatherInput(BaseModel):
    pcp: float = 0      # 1시간 강수량 (mm)
    wsd: float = 0      # 풍속 (m/s)
    tmp: float = 20     # 기온 (°C)
    pty: int = 0        # 강수형태 (0:없음 1:비 2:비/눈 3:눈 4:소나기)
    pop: int = 0        # 강수확률 (%)
    sky: int = 1        # 하늘상태 (1:맑음 3:구름많음 4:흐림)
    pm25: float = 0     # 미세먼지 PM2.5

# WEF 점수 계산 함수
def calculate_wef(data: WeatherInput) -> dict:
    score = 100

    # 강수량 감점
    if data.pcp >= 30:
        score -= 60
    elif data.pcp >= 10:
        score -= 40

    # 강수형태 + 강수확률 감점
    if data.pty != 0 and data.pop >= 70:
        score -= 20

    # 풍속 감점
    if data.wsd >= 13.9:
        score -= 40
    elif data.wsd >= 8:
        score -= 10

    # 폭염 감점
    if data.tmp >= 38:
        score -= 50
    elif data.tmp >= 35:
        score -= 35
    elif data.tmp >= 33:
        score -= 20

    # 한파 감점
    if data.tmp <= -15:
        score -= 45
    elif data.tmp <= -12:
        score -= 30

    # 대기질 감점
    if data.pm25 >= 76:       # 매우나쁨
        score -= 40
    elif data.pm25 >= 36:     # 나쁨
        score -= 20

    # 하늘상태
    if data.sky == 1:         # 맑음
        score += 5
    elif data.sky == 4:       # 흐림
        score -= 5

    # 0~100 범위로 제한
    score = max(0, min(100, score))

    # 등급 판정
    if score >= 70:
        label = "HIGH"
    elif score >= 40:
        label = "MID"
    else:
        label = "LOW"

    return {"score": score, "label": label}


# API 엔드포인트
@app.get("/")
def root():
    return {"message": "WePL WEF 엔진 작동 중 🌤️"}

@app.post("/wef")
def get_wef_score(data: WeatherInput):
    result = calculate_wef(data)
    return {
        "input": data,
        "wef_score": result["score"],
        "label": result["label"]
    }