# game-data1

유저가 고른 게임 몇 개를 바탕으로 **즐길 만한 똥겜**을 추천하는 모델을 만들기 위한 Steam 데이터 샘플입니다.
원본(약 2.2GB)에서 일부만 추출했습니다.

## 파일 구성 (`data/`)

| 파일 | 행 수 | 설명 |
|---|---|---|
| `games.csv` | 50,872 | 게임 기본 정보 (전체) — 평점 등급, 긍정 비율, 리뷰 수, 가격, 플랫폼 |
| `games_metadata.json` | 50,872 | 게임 설명과 태그 (JSON Lines, 전체) |
| `users.csv` | 20,000 | 샘플링된 유저 |
| `recommendations.csv` | 227,614 | 샘플 유저들이 작성한 리뷰 전부 (추천 여부, 플레이 시간) |

### 컬럼

- **games.csv**: `app_id, title, date_release, win, mac, linux, rating, positive_ratio, user_reviews, price_final, price_original, discount, steam_deck`
- **games_metadata.json**: `app_id, description, tags[]`
- **users.csv**: `user_id, products, reviews`
- **recommendations.csv**: `app_id, helpful, funny, date, is_recommended, hours, user_id, review_id`

## 샘플링 방법

- `games.csv`, `games_metadata.json`: 용량이 작아 전체를 그대로 포함
- `users.csv`: 리뷰를 5~200개 작성한 활성 유저(약 190만 명) 중 무작위 20,000명 (seed=42)
- `recommendations.csv`: 위 20,000명이 작성한 리뷰 전부

재현: `python scripts/extract_sample.py <원본 폴더> <출력 폴더> 20000`

## 똥겜 후보 참고 (games.csv `rating` 분포)

| rating | 게임 수 |
|---|---|
| Overwhelmingly Negative | 14 |
| Very Negative | 60 |
| Negative | 303 |
| Mostly Negative | 1,849 |
| Mixed | 12,157 |

## 출처

Kaggle "Game Recommendations on Steam" 데이터셋
