FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv export --format requirements-txt > requirements.txt
RUN uv pip install --system -r requirements.txt

COPY hair_classifier_v1.onnx hair_classifier_v1.onnx
COPY hair_classifier_v1.onnx.data hair_classifier_v1.onnx.data
COPY lambda_function.py lambda_function.py