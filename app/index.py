import json, glob, os, boto3
import numpy as np
br = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "ap-northeast-2"))
EMBED = os.environ.get("EMBED_MODEL", "amazon.titan-embed-text-v2:0")

def embed(text: str) -> list[float]:
    body = json.dumps({"inputText": text, "dimensions": 1024, "normalize": True})
    resp = br.invoke_model(modelId=EMBED, body=body)
    return json.loads(resp["body"].read())["embedding"]

def split(text: str, size=500, overlap=100):
    step = size - overlap
    return [text[i:i + size] for i in range(0, max(len(text) - overlap, 1), step)]

def build_index(doc_dir="docs", out="index", size=500, overlap=100):
    chunks = []
    for path in sorted(glob.glob(f"{doc_dir}/*.md")):
        for j, c in enumerate(split(open(path, encoding="utf-8").read(), size, overlap)):
            chunks.append({"id": f"{os.path.basename(path)}#{j}", "text": c})
    vecs = np.array([embed(c["text"]) for c in chunks], dtype=np.float32)
    os.makedirs(out, exist_ok=True)
    np.save(f"{out}/vectors.npy", vecs)
    json.dump(chunks, open(f"{out}/chunks.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{len(chunks)}개 조각 · {vecs.shape} → {out}/")

if __name__ == "__main__":
    build_index()