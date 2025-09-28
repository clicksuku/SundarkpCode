# LLM Zoomcamp 2025 – Payments Card Assistant (MCP + RAG + Eval/Monitoring)
The project takes input transaction details (CSV), Card details in JSON or Image. If the input is image, the image is sent to LLM OCR to derive the card details. 

The project leverages MCP to validate whether a card is valid using Luhns Algorithm. The MCP Server also check whether the card has any Risk or Compliance limit or transaction limits. If there is any risk or compliance error, it reaches out to the RAG (based on QDrant, which has ingested the Credit Card declined codes from schemes) to get the description in detail about the error. 

Finally the LLM observability is implemented using OPIK OpenSource. And Evaluation is also done using OPIK. 

This project was built to learn and experiment with LLM application patterns:
- Model Context Protocol (MCP) over Streamable HTTP
- Retrieval-Augmented Generation (RAG) with Qdrant
- Evaluation and Monitoring (Opik)

It ties together OCR-style card parsing via a vision-enabled LLM, card validation and risk checks via an MCP server, semantic retrieval over payments PDFs using Qdrant, and evaluation/monitoring of prompts and model outputs.

# Project Architecture

<img src="https://github.com/clicksuku/SundarkpCode/blob/master/LLM%20Zoomcamp%202025%20Project/_Project%20Images/LLM%20Evaluation%20Project.png" width="540" height="400" border="80" /></a>


## Features
- **MCP over Streamable HTTP**: Server exposes tools for card validation and risk checks
  - Server: `mcp_server/card_validation_mcp_server.py`
  - Tools: `isValidCardNumber`, `isCardActive`, `checkCardErrorCode`
- **RAG with Qdrant**: Indexes PDFs in `_pdfs/` and answers with context
  - RAG module: `rag/ragSolution.py`
  - Uses Qdrant 1.8+ HTTP on `http://localhost:6333`
- **Evaluation & Monitoring**: Uses Opik for tracking and metrics
  - Evaluation: `eval/llm_evaluation.py` with metrics (Hallucination, Answer Relevance, Context Precision/Recall)
  - Monitoring: Enable with `ENABLE_MONITORING=Yes` to track OpenAI calls via Opik
- **Card OCR / Parsing**: Uses OpenAI `gpt-4o-mini` image understanding to extract card JSON matching `cardDetails.schema.json`
  - Entry point: `paymentProcessWithLLM.py`

## Repository Structure
```
LLM Zoomcamp 2025/
├─ _pdfs/                      # Source documents for RAG
├─ _cardImages/                # Sample card images
├─ _transactions/              # CSV with card transactions for batch mode
├─ eval/
│  ├─ dataset.json             # Eval inputs
│  └─ llm_evaluation.py        # Evaluation runner (Opik)
├─ mcp_server/
│  └─ card_validation_mcp_server.py  # MCP server (FastMCP HTTP)
├─ prompts/                    # Prompt templates
├─ rag/
│  └─ ragSolution.py           # Qdrant ingestion + search
├─ cardDetails.schema.json     # JSON schema for card extraction
├─ paymentProcessWithLLM.py    # Main app (OCR + MCP + RAG + LLM response)
└─ README.md

## Prerequisites
- **Python** 3.10+
- **OpenAI** API access
- **Docker** (for running Qdrant locally)
- Optional: **Opik** local for monitoring (project calls `opik.configure(use_local=True)`)

## Environment Variables
Create a `.env` file in the project root or export env vars:
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
- Qdrant embedding API is used via `models.Document(text=..., model="BAAI/bge-small-en-v1.5")` in `rag/ragSolution.py`. Ensure your Qdrant version supports this API.

## Start Services
1) Start Qdrant (Docker):
```
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```
2) Start the MCP Server (HTTP, Streamable):
```
uv run mcp_server/card_validation_mcp_server.py
```
This exposes MCP at `http://127.0.0.1:8000/mcp` with tools used by the main app.

## Usage
`paymentProcessWithLLM.py` orchestrates OCR → MCP validation → RAG retrieval → final LLM answer.
- Image mode (OCR + validation + RAG + answer):
```
python paymentProcessWithLLM.py --type image --cardDetails _cardImages/Visa.jpg
```
- JSON mode (bypass OCR, use JSON directly):
```
python paymentProcessWithLLM.py --type json --cardDetails _cardImages/cardSample1.json
```
- CSV mode (iterate rows in `_transactions/Transactions data.csv`):
```
python paymentProcessWithLLM.py --type csv --cardDetails dummy
```
Notes:
- The first run will prepare the RAG index by reading PDFs from `_pdfs/` and creating a Qdrant collection `payments-rag`.
- Ensure the MCP server and Qdrant are running before executing `paymentProcessWithLLM.py`.

## Monitoring
- Set `ENABLE_MONITORING=Yes` in `.env` to wrap OpenAI calls with `opik.integrations.openai.track_openai`.
- Artifacts and screenshots are under `monitoring/`.

<img src="https://github.com/clicksuku/SundarkpCode/blob/master/LLM%20Zoomcamp%202025%20Project/monitoring/Screenshots/Eval%20Screenshot%201.png" width="540" height="400" border="80" /></a>

<img src="https://github.com/clicksuku/SundarkpCode/blob/master/LLM%20Zoomcamp%202025%20Project/monitoring/Screenshots/Eval%20Screenshot%202.png" width="540" height="400" border="80" /></a>

<img src="https://github.com/clicksuku/SundarkpCode/blob/master/LLM%20Zoomcamp%202025%20Project/monitoring/Screenshots/Card%20Conversion.png" width="540" height="400" border="80" /></a>


## Evaluation
To run evaluation with Opik metrics:
```
cd eval
python llm_evaluation.py
```
This reads `dataset.json`, creates/updates an Opik dataset, and runs `evaluate(...)` with multiple metrics against `gpt-4o-mini`.

<img src="https://github.com/clicksuku/SundarkpCode/blob/master/LLM%20Zoomcamp%202025%20Project/eval/screenshots/Evaluation%20Screeshot.png" width="540" height="400" border="80" /></a>


## Troubleshooting
- Qdrant connection error: confirm Docker is running and `localhost:6333` is reachable.
- MCP tool calls fail: ensure `card_validation_mcp_server.py` is running on `127.0.0.1:8000`.
- OpenAI auth/base URL errors: verify `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `.env`.
- PDF ingestion empty: verify there are PDFs in `_pdfs/`.

## License
For educational purposes within LLM Zoomcamp 2025. Adjust as needed.
