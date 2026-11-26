\# rag-guide 프로젝트 규칙



\## 기술 기준

\- Python 3.12, 외부 프레임워크(LangChain 등) 사용 금지

\- LLM 호출은 app/llm.py 한 곳에서만 한다 (boto3 bedrock-runtime)

\- 모델 ID와 리전은 환경변수에서 읽는다. 코드에 하드코딩 금지



\## 안전 기준

\- 자격 증명 · 키 · .env 파일은 읽거나 출력하지 않는다

\- 새 의존성 추가 전에 이유를 설명하고 승인을 받는다



\## 작업 방식

\- 코드를 바꾸면 eval/run\_eval.py 를 실행해 점수를 보고한다

\- AI가 만든 코드를 사람이 고친 경우 docs/ai-log.md 에 사유를 남긴다

