"""Steam 원본 데이터에서 일부만 추출해 GitHub 업로드용 샘플을 만든다.

- games.csv / games_metadata.json : 전체 게임 정보 (용량이 작아 그대로 복사)
- users.csv       : 리뷰 5~200개인 활성 유저 중 무작위 N명
- recommendations : 위 유저들이 작성한 리뷰 전부
"""
import csv
import random
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
N_USERS = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
SEED = 42

OUT.mkdir(parents=True, exist_ok=True)

shutil.copyfile(SRC / "games.csv", OUT / "games.csv")
shutil.copyfile(SRC / "games_metadata.json", OUT / "games_metadata.json")

# 1) 활성 유저 후보 수집
candidates = []
with open(SRC / "users.csv", newline="", encoding="utf-8") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        reviews = int(row[2])
        if 5 <= reviews <= 200:
            candidates.append(row)
print(f"candidate users: {len(candidates):,}")

random.seed(SEED)
sampled = random.sample(candidates, min(N_USERS, len(candidates)))
sampled.sort(key=lambda x: int(x[0]))
user_ids = {row[0] for row in sampled}

with open(OUT / "users.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(sampled)

# 2) 해당 유저들의 리뷰만 스트리밍 추출
kept = 0
with open(SRC / "recommendations.csv", newline="", encoding="utf-8") as fin, \
     open(OUT / "recommendations.csv", "w", newline="", encoding="utf-8") as fout:
    r = csv.reader(fin)
    w = csv.writer(fout)
    header = next(r)
    uid_idx = header.index("user_id")
    w.writerow(header)
    for row in r:
        if row[uid_idx] in user_ids:
            w.writerow(row)
            kept += 1
print(f"sampled users: {len(sampled):,}  recommendations kept: {kept:,}")
