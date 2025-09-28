# LLM Zoomcamp 2025 – Payments Card Assistant (MCP + RAG + Eval/Monitoring)

This project was built to learn and experiment with LLM application patterns:
- Model Context Protocol (MCP) over Streamable HTTP
- Retrieval-Augmented Generation (RAG) with Qdrant
- Evaluation and Monitoring (Opik)

It ties together OCR-style card parsing via a vision-enabled LLM, card validation and risk checks via an MCP server, semantic retrieval over payments PDFs using Qdrant, and evaluation/monitoring of prompts and model outputs.

## Features
- **MCP over Streamable HTTP**: Server exposes tools for card validation and risk checks
  - Server: `Project/mcp_server/card_validation_mcp_server.py`
  - Tools: `isValidCardNumber`, `isCardActive`, `checkCardErrorCode`
- **RAG with Qdrant**: Indexes PDFs in `Project/_pdfs/` and answers with context
  - RAG module: `Project/rag/ragSolution.py`
  - Uses Qdrant 1.8+ HTTP on `http://localhost:6333`
- **Evaluation & Monitoring**: Uses Opik for tracking and metrics
  - Evaluation: `Project/eval/llm_evaluation.py` with metrics (Hallucination, Answer Relevance, Context Precision/Recall)
  - Monitoring: Enable with `ENABLE_MONITORING=Yes` to track OpenAI calls via Opik
- **Card OCR / Parsing**: Uses OpenAI `gpt-4o-mini` image understanding to extract card JSON matching `Project/cardDetails.schema.json`
  - Entry point: `Project/readCardOCR.py`

## Repository Structure
```
LLM Zoomcamp 2025/
├─ Project/
│  ├─ _pdfs/                      # Source documents for RAG
│  ├─ _cardImages/                # Sample card images
│  ├─ _transactions/              # CSV with card transactions for batch mode
│  ├─ eval/
│  │  ├─ dataset.json             # Eval inputs
│  │  └─ llm_evaluation.py        # Evaluation runner (Opik)
│  ├─ mcp_server/
│  │  └─ card_validation_mcp_server.py  # MCP server (FastMCP HTTP)
│  ├─ monitoring/                 # Screenshots and exports
│  ├─ prompts/                    # Prompt templates
│  ├─ rag/
│  │  └─ ragSolution.py           # Qdrant ingestion + search
│  ├─ cardDetails.schema.json     # JSON schema for card extraction
│  └─ readCardOCR.py              # Main app (OCR + MCP + RAG + LLM response)
└─ (this) README.md
```

## Prerequisites
- **Python** 3.10+
- **OpenAI** API access
- **Docker** (for running Qdrant locally)
- Optional: **Opik** local for monitoring (project calls `opik.configure(use_local=True)`)

## Environment Variables
Create a `.env` file in the project root or export env vars:
```
OPENAI_API_KEY=sk-...
# If you use a gateway or Azure/OpenAI proxy, set the base URL; otherwise omit
OPENAI_BASE_URL=https://api.openai.com/v1

# Enable OpenAI call tracking via Opik
ENABLE_MONITORING=Yes
```

## Install Dependencies
Create a virtual environment and install packages:
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install python-dotenv openai fastmcp qdrant-client langchain langchain-community opik keras
```

Notes:
- Qdrant embedding API is used via `models.Document(text=..., model="BAAI/bge-small-en-v1.5")` in `ragSolution.py`. Ensure your Qdrant version supports this API.
- Keras is imported for `from keras import export` (present in code). If unused in your environment, you may safely remove that import.

## Start Services
1) Start Qdrant (Docker):
```
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

2) Start the MCP Server (HTTP, Streamable):
```
python Project/mcp_server/card_validation_mcp_server.py
```
This exposes MCP at `http://127.0.0.1:8000/mcp` with tools used by the main app.

## Usage
`readCardOCR.py` orchestrates OCR → MCP validation → RAG retrieval → final LLM answer.

- Image mode (OCR + validation + RAG + answer):
```
python Project/readCardOCR.py --type image --cardDetails Project/_cardImages/Visa.jpg
```

- JSON mode (bypass OCR, use JSON directly):
```
python Project/readCardOCR.py --type json --cardDetails Project/_cardImages/cardSample1.json
```

- CSV mode (iterate rows in `Project/_transactions/Transactions data.csv`):
```
python Project/readCardOCR.py --type csv --cardDetails dummy
```
Notes:
- The first run will prepare the RAG index by reading PDFs from `Project/_pdfs/` and creating a Qdrant collection `payments-rag`.
- Ensure the MCP server and Qdrant are running before executing `readCardOCR.py`.

## Evaluation
To run evaluation with Opik metrics:
```
cd Project/eval
python llm_evaluation.py
```
This reads `dataset.json`, creates/updates an Opik dataset, and runs `evaluate(...)` with multiple metrics against `gpt-4o-mini`.

## Monitoring
- Set `ENABLE_MONITORING=Yes` in `.env` to wrap OpenAI calls with `opik.integrations.openai.track_openai`.
- Artifacts and screenshots are under `Project/monitoring/`.

## Troubleshooting
- Qdrant connection error: confirm Docker is running and `localhost:6333` is reachable.
- MCP tool calls fail: ensure `card_validation_mcp_server.py` is running on `127.0.0.1:8000`.
- OpenAI auth/base URL errors: verify `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `.env`.
- PDF ingestion empty: verify there are PDFs in `Project/_pdfs/`.

## License
For educational purposes within LLM Zoomcamp 2025. Adjust as needed.
