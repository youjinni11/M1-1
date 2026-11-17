# 데이터 출처 및 수집 방법

## 파일

- `DEXKOUS_2020_2025.csv` — 원/달러 현물 환율 일별 데이터 (2020-01-02 ~ 2025-12-31, 1,565행)
  - `observation_date`: 날짜 (YYYY-MM-DD, 평일)
  - `DEXKOUS`: 1달러당 원화 (빈칸 = 미국 연방 공휴일로 고시 없음, 66건)

## 출처

- **FRED (Federal Reserve Economic Data)**, Federal Reserve Bank of St. Louis
- 시리즈: `DEXKOUS` — *South Korean Won to U.S. Dollar Spot Exchange Rate*
- 원 자료: Board of Governors of the Federal Reserve System (US), H.10 Foreign Exchange Rates
- 단위: South Korean Won to One U.S. Dollar, 일별, 계절조정 없음
- 시리즈 페이지: https://fred.stlouisfed.org/series/DEXKOUS

## 다시 받는 방법 (재현)

1. 브라우저에서 아래 주소를 열면 같은 CSV가 내려받아집니다.
   ```
   https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXKOUS&cosd=2020-01-01&coed=2025-12-31
   ```
2. 또는 시리즈 페이지에서 기간을 2020-01-01 ~ 2025-12-31로 설정 → `Download` → `CSV`.
3. 파일 이름을 `DEXKOUS_2020_2025.csv`로 바꿔 이 폴더에 넣습니다.

> 과거 값이 사후에 수정될 수 있어(revision), 나중에 내려받으면 일부 값이 다를 수 있습니다.
> 수집 시점 검증값: 유효값 1,499개, 합계 1,926,117.85, 최소 1,081.62, 최대 1,481.45

## 라이선스 / 이용 주의

- 이 데이터는 미국 연방준비제도(Federal Reserve Board)가 공개한 자료를 FRED가 제공하는 것입니다.
- FRED 이용약관(https://fred.stlouisfed.org/legal/)에 따라 **출처 표기 후 학습·비상업 분석 목적**으로 사용했습니다.
- 재배포·상업적 이용 시에는 FRED 및 원 자료 제공기관의 약관을 직접 확인하세요.
