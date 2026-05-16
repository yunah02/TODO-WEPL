# 날씨연동형 TO-DO 어플 : 웨플(WEPL)

# 연습형이라 업로드 계속 진행 중

# 개발 동기
  최근 몇 년간 기후변화의 영향으로 갑작스러운 폭우, 폭염, 한파 등 이상기후 현상이 일상적으로 발생하고 있다. 2025년도 이상기후 보고서에 따르면, 연평균 기온이 2023년에 13.7도에서 2024년에는 14.5로 상승했다고 한다. 더불어, 폭염과 집중호우 또는 태풍과 같이 인간의 일상생활에 큰 영향을 미치는 극한기상 현상이 증가할 것이라고 보고했다. 이러한 변화는 단순한 날씨 차원을 넘어, 개인의 일정 계획과 사회적 활동 전반에 직간접적인 영향을 미치고 있다. 예기치 못한 비나 미세먼지로 인해 야외 운동이 취소되거나, 친구와의 약속 장소를 변경해야 하는 상황이 잦아지고 있으며, 이는 곧 일정 관리의 번거로움과 실행 실패율 증가로 이어지고 있다.

그러나 현재 시중에 존재하는 대부분의 To-Do 관리 서비스는 일정 등록, 알림, 동기화 등 효율 중심 기능에 집중되어 있다. 단순히 “무엇을 해야 하는가”에 초점을 맞춘 기능 위주로 구성되어 있다. 따라서 사용자 입장에서는 “오늘 계획이 날씨에 적합한가?”, “대체로 어떤 일정으로 바꾸면 좋을까?”에 대한 해답을 스스로 찾아야 하는 불편함이 지속된다.

이에 단순한 일정 관리 도구를 넘어, 날씨 변화에 선제적으로 대응하며 개인의 루틴과 선호를 반영하는 지능형 To-Do 시스템의 필요성을 인식하였다. ‘웨플(Wepl: Weather + Plan)’은 이러한 문제의식에서 출발하였다. 웨플은 날씨 데이터를 기반으로 일정 실행 가능성을 자동 판단하고, 상황에 따라 시간·장소·활동 대안을 제시하는 개인 맞춤형 일정 관리 앱으로, 사용자가 복잡한 판단 없이 “지금 가능한 최적의 일정”을 실행할 수 있도록 돕는 것을 목표로 한다.


# ✨ 핵심 기능 
### 1. 🗒️ 스마트 투두 관리
단순히 할 일만 입력하는 것이 아닌, **맥락 정보를 함께 등록**합니다.
 
- 제목, 카테고리, 장소, 시작/종료 시간 입력
- 참여 인원, 목적, 메모 등 세부 정보 등록
- 장소 미입력 시 기본 지역(홈) 자동 설정
- 날짜별 투두 목록 캘린더 형식으로 조회
---
 
### 2. 📊 실행가능성 분석 (WEF Score)
기상청 + 에어코리아 API 데이터를 기반으로 **투두별 실행 가능성을 0~100점으로 자동 산출**합니다.
 
| 등급 | 점수 범위 | 표시 색상 |
|------|-----------|-----------|
| 🟢 HIGH | 70 ~ 100점 | 초록 |
| 🟡 MID | 40 ~ 69점 | 노랑 |
| 🔴 LOW | 0 ~ 39점 | 빨강 |
 
**점수 계산 기준 (WEF Score)**
 
| 기상 요소 | 조건 | 감점 |
|-----------|------|------|
| 강수량 | ≥ 10mm/h | -40점 |
| 강수량 | ≥ 30mm/h | -60점 |
| 강수형태 + 강수확률 | PTY ≠ 0 & POP = 70 | -20점 |
| 풍속 | ≥ 8m/s / 13.9m/s | -10 / -40점 |
| 폭염 | 33°C / 35°C / 38°C | -20 / -35 / -50점 |
| 한파 | ≤ -12°C / -15°C | -30 / -45점 |
| 대기질 | 나쁨 / 매우나쁨 | -20 / -40점 |
| 하늘상태 | 맑음 / 흐림 | +5 / -5점 |
 
```
WEF = clamp(100 + Σ(보정치), 0, 100)
```
 
---
 
### 3. 🤖 AI 기반 대체일정 추천
실행가능성이 낮아진 투두에 대해 **CLOVA X AI가 대체 활동 4가지와 장소 4곳을 자동 추천**합니다.
 
- 사용자의 선호도(분위기, 활동 스타일, 일정 유형) 반영
- 현재 날씨 조건(실내/실외 적합 여부) 반영
- 원래 일정의 **목적은 유지**하면서 실행 방식만 변경
- 장소 선택 시 투두 데이터 자동 업데이트
**추천 흐름**
```
대체 제안 버튼 클릭
    → 사용자 선호도 + 투두 맥락 + 날씨 데이터 분석
    → CLOVA X 프롬프트 생성 및 API 호출
    → 대체 활동 4가지 제안
    → 활동 선택 시 근처 장소 4곳 추천
    → 장소 확정 시 투두 자동 업데이트
```
 
---
 
### 4. 🔔 스마트 알림 기능
스케줄러가 **3시간마다 날씨를 재분석**해 실행가능성 변화를 감지하고 자동으로 알림을 보냅니다.
 
- **데일리 브리핑**: 매일 아침 8시, 오늘 일정 실행가능성 요약 알림
- **날씨 변동 알림**: HIGH/MID → LOW로 하락 시 즉시 FCM 푸시 알림
- 짧은 시간 내 중복 알림 방지 (Redis cooldown 처리)
- 알림 터치 시 해당 투두 상세 화면으로 이동
<br>
## 🛠️ 기술 스택
 
### Frontend
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat&logo=flutter&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
 
### Backend
![Java](https://img.shields.io/badge/Java_21-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat&logo=spring-boot&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring_Security-6DB33F?style=flat&logo=spring-security&logoColor=white)
 
### Database
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
 
### DevOps & Infra
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![AWS ECS](https://img.shields.io/badge/AWS_ECS-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)
 
### External API
| API | 용도 |
|-----|------|
| 기상청 단기예보 API | 강수확률, 강수량, 기온, 풍속, 하늘상태 |
| 에어코리아 API | PM10, PM2.5, 오존 대기질 |
| CLOVA X API | 대체 활동 및 장소 AI 추천 |
| Firebase FCM | 푸시 알림 전송 |
 
<br>
## 🗂️ 프로젝트 구조
 
```
TODO-WEPL/
├── backend/           # Spring Boot 백엔드
│   ├── src/
│   │   └── main/java/
│   │       ├── controller/    # API 엔드포인트
│   │       ├── service/       # 비즈니스 로직
│   │       ├── domain/        # 엔티티
│   │       └── repository/    # DB 접근
│   └── build.gradle
├── frontend/          # Flutter 앱
│   └── lib/
├── main.py            # FastAPI WEF 점수 계산 엔진
├── requirements.txt
└── README.md
```
 
<br>
## 🚀 시작하기
 
### 요구사항
- Python 3.10+
- Java 21
- Flutter SDK
- PostgreSQL
- Redis
### 백엔드 실행
```bash
# FastAPI (WEF 엔진)
pip install -r requirements.txt
uvicorn main:app --reload
 
# Spring Boot
./gradlew bootRun
```
 
### 프론트엔드 실행
```bash
cd frontend
flutter pub get
flutter run
```