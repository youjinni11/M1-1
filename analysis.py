"""
원/달러 환율(USD/KRW) 2020~2025 시계열 분석 스크립트

실행:  python analysis.py
결과:  images/ 폴더에 그래프 PNG 저장, outputs/ 폴더에 요약 통계 CSV 저장,
       터미널에 리포트에 인용한 주요 수치 출력

데이터: data/DEXKOUS_2020_2025.csv
        (FRED, Board of Governors of the Federal Reserve System, 시리즈 DEXKOUS)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 화면 없이 PNG 파일로만 저장
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "DEXKOUS_2020_2025.csv"
IMG = BASE / "images"
OUT = BASE / "outputs"
IMG.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

# 그래프 라벨은 한글 폰트가 없는 PC에서도 깨지지 않도록 영어로 작성
plt.rcParams.update({"figure.dpi": 110, "axes.grid": True, "grid.alpha": 0.3})


def section(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# ---------------------------------------------------------------------
# 1. 데이터 불러오기 & 기본 정보 확인
# ---------------------------------------------------------------------
section("1. 데이터 기본 정보")
raw = pd.read_csv(DATA, parse_dates=["observation_date"])
raw = raw.rename(columns={"observation_date": "date", "DEXKOUS": "rate"})
raw["rate"] = pd.to_numeric(raw["rate"], errors="coerce")  # 빈칸 -> NaN
raw = raw.sort_values("date").reset_index(drop=True)

print(f"기간: {raw.date.min().date()} ~ {raw.date.max().date()}")
print(f"전체 행 수(평일 기준): {len(raw)}")
print(f"컬럼: {list(raw.columns)}  / dtypes: {dict(raw.dtypes.astype(str))}")
print(f"날짜 중복: {raw.date.duplicated().sum()}건, 날짜 정렬 여부: {raw.date.is_monotonic_increasing}")

# ---------------------------------------------------------------------
# 2. 결측치 처리
#    - FRED H.10 환율은 미국 연방 공휴일에 고시되지 않아 빈칸이 생긴다.
#    - '거래가 없던 날'이므로 값을 만들어 넣지 않고 제거(dropna)한다.
#      (보간하면 존재하지 않는 가격을 만들어 변화율이 왜곡됨)
# ---------------------------------------------------------------------
section("2. 결측치")
missing = raw[raw.rate.isna()]
print(f"결측치: {len(missing)}건 ({len(missing)/len(raw):.1%})")
print("결측 날짜 예시:", [d.strftime("%Y-%m-%d") for d in missing.date.head(8)])
print("결측 요일 분포:", missing.date.dt.day_name().value_counts().to_dict())
missing[["date"]].to_csv(OUT / "missing_dates.csv", index=False)

df = raw.dropna().set_index("date")
print(f"정제 후 데이터 포인트: {len(df)}개")

# ---------------------------------------------------------------------
# 3. 파생 변수 (시계열 분석 기법)
#    (1) 이동평균 20/60/120일  (2) 일간 변화율(%)  (3) 20일 변동성
#    (4) 월별/연도별 구간 통계
# ---------------------------------------------------------------------
df["ma20"] = df.rate.rolling(20).mean()     # 약 1개월 (거래일 20일)
df["ma60"] = df.rate.rolling(60).mean()     # 약 1분기
df["ma120"] = df.rate.rolling(120).mean()   # 약 반년
df["ret"] = df.rate.pct_change() * 100      # 일간 변화율(%)
df["vol20"] = df.ret.rolling(20).std()      # 최근 20거래일 변화율의 표준편차 = 변동성

# ---------------------------------------------------------------------
# 4. 이상치 점검
#    기준: 일간 변화율의 z-score 절댓값 > 3 (평균에서 표준편차 3배 이상 벗어남)
#    판단: 입력 오류가 아니라 실제 시장 급변으로 보이면 '삭제하지 않고 표시만' 한다.
#          (환율 급변 자체가 분석 대상이므로 지우면 정보 손실)
# ---------------------------------------------------------------------
section("3. 이상치 (일간 변화율 |z| > 3)")
z = (df.ret - df.ret.mean()) / df.ret.std()
df["outlier"] = z.abs() > 3
outliers = df.loc[df.outlier, ["rate", "ret"]].copy()
outliers["z"] = z[df.outlier].round(2)
print(f"이상치 후보: {len(outliers)}건")
print(outliers.round(2).to_string())
outliers.round(3).to_csv(OUT / "outliers.csv")
# 가격 수준 자체의 오입력 점검 (예: 0, 음수, 10배 튐)
print(f"가격 범위: {df.rate.min():.2f} ~ {df.rate.max():.2f} (비정상 값 없음 확인용)")

# ---------------------------------------------------------------------
# 5. 연도별 구간 통계
# ---------------------------------------------------------------------
section("4. 연도별 구간 통계")
yearly = df.groupby(df.index.year).agg(
    start=("rate", "first"), end=("rate", "last"), mean=("rate", "mean"),
    min=("rate", "min"), max=("rate", "max"), daily_vol=("ret", "std"),
)
yearly["change_%"] = (yearly.end / yearly.start - 1) * 100
yearly["range"] = yearly["max"] - yearly["min"]
print(yearly.round(2).to_string())
yearly.round(3).to_csv(OUT / "yearly_stats.csv")

total = (df.rate.iloc[-1] / df.rate.iloc[0] - 1) * 100
print(f"\n전체 기간 변화: {df.rate.iloc[0]:.2f} -> {df.rate.iloc[-1]:.2f} ({total:+.1f}%)")
print(f"최저: {df.rate.idxmin().date()} {df.rate.min():.2f} / 최고: {df.rate.idxmax().date()} {df.rate.max():.2f}")

# 이동평균 기준 상승 구간 비율 (종가가 120일선 위에 있던 날의 비율)
above = (df.rate > df.ma120).loc[df.ma120.notna()]
print(f"120일 이동평균 위에 있던 날 비율: {above.mean():.1%}")

# ---------------------------------------------------------------------
# 6. 변동성 상위 구간
# ---------------------------------------------------------------------
section("5. 변동성(20일) 상위 구간")
vol_month = df.vol20.resample("ME").max()
print(vol_month.sort_values(ascending=False).head(8).round(3).to_string())
print(f"\n20일 변동성 중앙값: {df.vol20.median():.3f}%")
top_moves = df.ret.abs().sort_values(ascending=False).head(10)
print("\n일간 변화율 절댓값 TOP10:")
print(df.loc[top_moves.index, ["rate", "ret"]].round(2).to_string())

# ---------------------------------------------------------------------
# 7. 월별(달력 월) 변화율 패턴
# ---------------------------------------------------------------------
section("6. 달력 월별 평균 변화율")
monthly_last = df.rate.resample("ME").last()
monthly_ret = monthly_last.pct_change().dropna() * 100
by_month = monthly_ret.groupby(monthly_ret.index.month).agg(["mean", "median", "std", "count"])
by_month["up_ratio"] = monthly_ret.groupby(monthly_ret.index.month).apply(lambda s: (s > 0).mean())
print(by_month.round(2).to_string())
by_month.round(3).to_csv(OUT / "calendar_month_returns.csv")
print(f"\n월간 변화율 전체 표준편차: {monthly_ret.std():.2f}%")

# =====================================================================
# 시각화
# =====================================================================
EVENTS = {  # 그래프에 표시할 외부 이벤트 (해석 '가설'용, 인과관계 증명 아님)
    "2020-03-19": "COVID-19 shock",
    "2022-10-25": "Fed rapid hikes\n(2022 peak)",
    "2024-12-03": "Martial law\ndeclared (KR)",
    "2025-04-08": "US tariff\nturmoil",
}

# --- 그림 1: 환율 추이 + 이동평균 ---------------------------------
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.plot(df.index, df.rate, color="#9aa5b1", lw=0.9, label="Daily rate")
ax.plot(df.index, df.ma20, color="#2b8cbe", lw=1.2, label="MA 20 (~1 month)")
ax.plot(df.index, df.ma120, color="#d7301f", lw=1.8, label="MA 120 (~6 months)")
for d, label in EVENTS.items():
    d = pd.Timestamp(d)
    y = df.rate.asof(d)
    ax.annotate(label, xy=(d, y), xytext=(d, y + 55), fontsize=8.5, ha="center",
                arrowprops=dict(arrowstyle="->", color="#555"), color="#333")
ax.set_title("USD/KRW exchange rate 2020-2025 with moving averages")
ax.set_ylabel("KRW per 1 USD")
ax.set_ylim(df.rate.min() - 30, df.rate.max() + 90)  # 0부터 시작하면 변화가 평평해 보여 값 범위에 맞춤
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(IMG / "01_rate_trend_ma.png")
plt.close(fig)

# --- 그림 2: 일간 변화율 + 20일 변동성 ------------------------------
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True,
                             gridspec_kw={"height_ratios": [1.2, 1]})
a1.bar(df.index, df.ret, width=1.5, color=np.where(df.ret >= 0, "#d7301f", "#2b8cbe"))
a1.scatter(df.index[df.outlier], df.ret[df.outlier], s=18, color="black", zorder=3,
           label="|z| > 3 (outlier candidate)")
a1.set_ylabel("Daily change (%)")
a1.set_title("Daily % change (red = KRW weaker) and 20-day volatility")
a1.legend(loc="upper left")
a2.plot(df.index, df.vol20, color="#6a51a3", lw=1.2)
a2.axhline(df.vol20.median(), color="gray", ls="--", lw=1, label=f"median {df.vol20.median():.2f}%")
a2.set_ylabel("20-day std of daily change (%)")
a2.legend(loc="upper left")
fig.tight_layout()
fig.savefig(IMG / "02_daily_change_volatility.png")
plt.close(fig)

# --- 그림 3: 연도별 박스플롯 + 연간 변화율 ---------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8))
years = sorted(df.index.year.unique())
a1.boxplot([df.rate[df.index.year == y] for y in years], tick_labels=years)
a1.set_title("Rate distribution by year")
a1.set_ylabel("KRW per 1 USD")
colors = ["#d7301f" if v > 0 else "#2b8cbe" for v in yearly["change_%"]]
a2.bar([str(y) for y in years], yearly["change_%"], color=colors)
for i, v in enumerate(yearly["change_%"]):
    a2.text(i, v + (0.3 if v > 0 else -0.9), f"{v:+.1f}%", ha="center", fontsize=9)
a2.axhline(0, color="black", lw=0.8)
a2.set_title("Year-over-year change (first -> last trading day)")
a2.set_ylabel("%")
fig.tight_layout()
fig.savefig(IMG / "03_yearly_stats.png")
plt.close(fig)

# --- 그림 4: 달력 월별 평균 변화율 -----------------------------------
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.bar(by_month.index, by_month["mean"], yerr=by_month["std"], capsize=3,
       color=["#d7301f" if v > 0 else "#2b8cbe" for v in by_month["mean"]], alpha=0.85)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(range(1, 13))
ax.set_xlabel("Calendar month")
ax.set_ylabel("Mean monthly change (%)  (error bar = 1 std)")
ax.set_title("Is there a calendar-month pattern? (2020-2025, n = 5~6 per month)")
fig.tight_layout()
fig.savefig(IMG / "04_calendar_month_pattern.png")
plt.close(fig)

# =====================================================================
# 보너스: (A) 시계열 분해  (B) 베이스라인 예측
# =====================================================================
section("7. [보너스 A] 시계열 분해 (월평균, 가법 모형)")
# 월평균으로 집계 -> 12개월 중심 이동평균 = 추세 / 추세 제거 후 월별 평균 = 계절성 / 나머지 = 노이즈
m = df.rate.resample("ME").mean()
trend = m.rolling(12, center=True).mean().rolling(2, center=True).mean()  # 2x12 MA (짝수 주기 중심화)
detr = m - trend
seasonal_idx = detr.groupby(detr.index.month).mean()
seasonal_idx -= seasonal_idx.mean()  # 계절성 합이 0이 되도록 보정
seasonal = pd.Series(seasonal_idx.loc[m.index.month].values, index=m.index)
resid = m - trend - seasonal
print("월별 계절성 지수(원):", seasonal_idx.round(1).to_dict())
print(f"계절성 진폭(최대-최소): {seasonal_idx.max() - seasonal_idx.min():.1f}원")
print(f"추세 범위: {trend.min():.1f} ~ {trend.max():.1f}원 (폭 {trend.max() - trend.min():.1f}원)")
print(f"잔차(노이즈) 표준편차: {resid.std():.1f}원")
print(f"분산 비교 - 추세: {trend.var():.0f}, 계절성: {seasonal.var():.0f}, 잔차: {resid.var():.0f}")

fig, axes = plt.subplots(4, 1, figsize=(12, 9), sharex=True)
for a, s, t in zip(axes, [m, trend, seasonal, resid],
                   ["Observed (monthly mean)", "Trend (2x12 MA)", "Seasonal (avg by month)", "Residual (noise)"]):
    a.plot(s.index, s.values, color="#333")
    a.set_title(t, fontsize=10, loc="left")
axes[3].axhline(0, color="gray", lw=0.8)
fig.suptitle("Classical additive decomposition of USD/KRW (monthly)")
fig.tight_layout()
fig.savefig(IMG / "05_decomposition.png")
plt.close(fig)

section("8. [보너스 B] 베이스라인 예측 (마지막 20거래일 홀드아웃)")
H = 20
train, test = df.rate.iloc[:-H], df.rate.iloc[-H:]
naive = pd.Series(train.iloc[-1], index=test.index)                     # 마지막 값 유지
ma_fc = pd.Series(train.iloc[-20:].mean(), index=test.index)           # 최근 20일 평균
slope = (train.iloc[-1] - train.iloc[-121]) / 120                      # 최근 120일 평균 기울기
drift = pd.Series(train.iloc[-1] + slope * np.arange(1, H + 1), index=test.index)


def mae(p):
    return (p - test).abs().mean()


def mape(p):
    return ((p - test).abs() / test).mean() * 100


fc = pd.DataFrame({"model": ["Naive (last value)", "MA20 mean", "Drift (120d slope)"],
                   "MAE_KRW": [mae(naive), mae(ma_fc), mae(drift)],
                   "MAPE_%": [mape(naive), mape(ma_fc), mape(drift)]})
print(f"학습 구간 끝: {train.index[-1].date()} ({train.iloc[-1]:.2f}), 테스트: {test.index[0].date()} ~ {test.index[-1].date()}")
print(fc.round(2).to_string(index=False))
fc.round(3).to_csv(OUT / "forecast_baseline.csv", index=False)

fig, ax = plt.subplots(figsize=(11, 4.8))
ax.plot(train.iloc[-120:].index, train.iloc[-120:], color="#333", label="Train (last 120 days)")
ax.plot(test.index, test, color="black", lw=2, label="Actual (test)")
ax.plot(test.index, naive, ls="--", label=f"Naive  MAE {mae(naive):.1f}")
ax.plot(test.index, ma_fc, ls="--", label=f"MA20   MAE {mae(ma_fc):.1f}")
ax.plot(test.index, drift, ls="--", label=f"Drift  MAE {mae(drift):.1f}")
ax.set_title(f"Baseline forecast for the last {H} trading days")
ax.set_ylabel("KRW per 1 USD")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(IMG / "06_baseline_forecast.png")
plt.close(fig)

section("완료")
print("images/ :", sorted(p.name for p in IMG.glob("*.png")))
print("outputs/:", sorted(p.name for p in OUT.glob("*.csv")))
