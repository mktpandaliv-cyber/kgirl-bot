"""K-girl Discord 잡담 자동 게시 스크립트.

질문 목록(questions.json)에서 날짜 기준으로 하나를 골라 디스코드 웹훅으로 올립니다.
날짜로 순서를 정하므로 100일 동안 같은 질문이 반복되지 않습니다.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
BOT_NAME = "運営パンダ"

if not WEBHOOK_URL:
    sys.exit("DISCORD_WEBHOOK_URL 이 설정되지 않았습니다.")

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "questions.json"), encoding="utf-8") as f:
    questions = json.load(f)

today_jst = datetime.now(timezone(timedelta(hours=9))).date()
question = questions[today_jst.toordinal() % len(questions)]

payload = {
    "username": BOT_NAME,
    "content": f"🐼 **今日の質問**\n\n{question}\n\n気軽にコメントしてね！",
}

req = urllib.request.Request(
    WEBHOOK_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "kgirl-bot"},
    method="POST",
)
with urllib.request.urlopen(req) as res:
    print(f"게시 완료 ({res.status}): {question}")
