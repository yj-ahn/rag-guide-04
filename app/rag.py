import json, os
import numpy as np
from app.index import embed
from app.llm import ask

INDEX_DIR = os.environ.get("INDEX_DIR", "index")          # Lab 4 Task 2 · Lab 5 Task 4 에서 다른 색인을 쓸 때 바꿉니다
VECS = np.load(f"{INDEX_DIR}/vectors.npy")
CHUNKS = json.load(open(f"{INDEX_DIR}/chunks.json", encoding="utf-8"))
PROMPT = open(f"prompts/{os.environ.get('PROMPT_VERSION', 'v1')}.txt", encoding="utf-8").read()
TOP_K = int(os.environ.get("TOP_K", "4"))                  # Lab 5 Task 3 에서 ConfigMap 으로 바꿉니다

def search(q: str, k=None, min_score=0.15):
    k = k or TOP_K
    s = VECS @ np.array(embed(q), dtype=np.float32)        # 정규화 벡터 → 내적 = 코사인
    top = np.argsort(-s)[:k]
    return [dict(CHUNKS[i], score=float(s[i])) for i in top if s[i] >= min_score]

def answer(q: str) -> dict:
    hits = search(q)
    if not hits:
        return {"answer": "규정에서 찾을 수 없습니다.", "sources": []}
    ctx = "\n\n".join(f"<발췌 id='{h['id']}'>\n{h['text']}\n</발췌>" for h in hits)
    r = ask(PROMPT, f"{ctx}\n\n<질문>{q}</질문>", max_tokens=700)
    return {"answer": r["text"], "sources": [h["id"] for h in hits], "usage": r["usage"]}