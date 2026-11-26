import json, re
from jsonschema import validate, ValidationError
from app.llm import ask

SCHEMA = json.load(open("schema/complaint.json", encoding="utf-8"))
SYSTEM = open("prompts/classify.txt", encoding="utf-8").read().replace("{스키마}", json.dumps(SCHEMA, ensure_ascii=False))
FALLBACK = {"decision": "보류", "reason": "자동 분류 실패", "confidence": "낮음", "needs_human": True}

def parse(text):
    m = re.search(r"\{.*\}", text, re.S)          # 앞뒤 설명 문장 제거
    obj = json.loads(m.group(0)) if m else None
    validate(obj, SCHEMA)
    return obj

def classify(complaint: str) -> dict:
    user = f"<민원>\n{complaint}\n</민원>"
    for attempt in range(2):
        r = ask(SYSTEM, user, max_tokens=800)
        try:
            return parse(r["text"])
        except (ValueError, TypeError, ValidationError) as e:
            user += f"\n\n이전 출력이 스키마에 맞지 않았습니다: {str(e)[:150]}. JSON만 다시 출력하세요."
    return FALLBACK