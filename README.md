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

Python 3.10 이상이 필요합니다. 운영체제에 맞는 쪽을 따라 하세요.

### Mac / Linux (터미널)

Mac에서는 `python`, `pip` 대신 **`python3`**, **`pip3`** 를 사용합니다.

```bash
# 1. 저장소 받기
git clone https://github.com/youjinni11/M1-1.git
cd M1-1

# 2. 라이브러리 설치
python3 -m pip install -r requirements.txt

# 3. 분석 실행 -> images/, outputs/ 다시 생성 + 주요 수치 터미널 출력
python3 analysis.py
```

설치 시 `externally-managed-environment` 오류가 나면 가상환경을 만들어 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analysis.py
```

### Windows (PowerShell 또는 명령 프롬프트)

Windows에서는 **`py`** 명령을 사용합니다. (`python`이 안 되면 `py`로 시도)

```powershell
# 1. 저장소 받기
git clone https://github.com/youjinni11/M1-1.git
cd M1-1

# 2. 라이브러리 설치
py -m pip install -r requirements.txt

# 3. 분석 실행 -> images\, outputs\ 다시 생성 + 주요 수치 터미널 출력
py analysis.py
```

가상환경을 쓰려면 다음과 같이 합니다.

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python analysis.py
```

PowerShell에서 `activate` 실행이 막히면 `Set-ExecutionPolicy -Scope Process RemoteSigned` 를 먼저 입력하세요(현재 창에서만 적용).

### 실행 결과 확인

- 터미널에 분석 수치가 출력되고 마지막에 `완료`와 생성된 파일 목록이 나옵니다.
- `images/`에 그래프 6개, `outputs/`에 요약 CSV 5개가 다시 생성됩니다.
- 처음 실행 시 `Matplotlib is building the font cache` 메시지와 pip 업데이트 안내는 무시해도 됩니다.

## 개발 환경

- Python 3.10+ (실행 확인: Python 3.13 Linux, Python 3.14 macOS. Windows는 미확인)
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
