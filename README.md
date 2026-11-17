# M1-1 · 원/달러 환율 2020~2025 시계열 트렌드 분석

코디세이 AI 응용 미션 **"AI 데이터 분석: 데이터 기반 트렌드 분석"** 제출 저장소입니다.

- 📄 **분석 리포트:** [REPORT.md](REPORT.md)
- 🐍 **분석 코드:** [analysis.py](analysis.py)
- 📊 **그래프:** [images/](images/) (6개)
- 📁 **데이터 & 출처:** [data/](data/) · [data/README.md](data/README.md)

## 폴더 구조

```
M1-1/
├── data/
│   ├── DEXKOUS_2020_2025.csv     # 원본 데이터 (FRED)
│   └── README.md                 # 출처·수집 방법·라이선스
├── images/                       # analysis.py 실행 시 생성되는 그래프
│   ├── 01_rate_trend_ma.png
│   ├── 02_daily_change_volatility.png
│   ├── 03_yearly_stats.png
│   ├── 04_calendar_month_pattern.png
│   ├── 05_decomposition.png      # 보너스: 시계열 분해
│   └── 06_baseline_forecast.png  # 보너스: 베이스라인 예측
├── outputs/                      # 요약 통계 CSV (실행 시 생성)
├── analysis.py                   # 전체 분석 스크립트
├── REPORT.md                     # 분석 리포트
├── requirements.txt
└── README.md
```

## 실행 방법

Python 3.10 이상이 필요합니다.

```bash
# 1. 저장소 받기
git clone https://github.com/youjinni11/M1-1.git
cd M1-1

# 2. (선택) 가상환경
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. 라이브러리 설치
pip install -r requirements.txt

# 4. 분석 실행 -> images/, outputs/ 다시 생성 + 주요 수치 터미널 출력
python analysis.py
```

## 개발 환경

- Python 3.10+ (작성·검증: Python 3.13)
- pandas, numpy, matplotlib (`requirements.txt`)
- 그래프 라벨은 한글 폰트가 없는 환경에서도 깨지지 않도록 영어로 작성했습니다.

## 분석 요약

| 질문 | 답 |
|------|----|
| Q1 추세가 있었나? | 있음. 6년간 +24.8% (1,157.95 → 1,444.55원), 연평균은 2021년 제외 매년 상승 |
| Q2 언제 크게 흔들렸나? | 2020-03~04, 2022-11~12, 2025-05 — 20일 변동성이 평소(0.50%)의 2배 이상 |
| Q3 오를 때·내릴 때 다른가? | 큰 하루 변동 TOP10 중 9개가 하락(원화 강세) → "천천히 오르고 급하게 내린다" |
| Q4 월별 계절성이 있나? | 근거 약함. 월별 편차 < 표준편차, 분해 시 계절성 분산은 잔차의 약 1/8 |

## 데이터 출처

FRED, Federal Reserve Bank of St. Louis — `DEXKOUS` (원 자료: Board of Governors of the Federal Reserve System, H.10). 자세한 내용과 라이선스 주의 문구는 [data/README.md](data/README.md) 참고.
