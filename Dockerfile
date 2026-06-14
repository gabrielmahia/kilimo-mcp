# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for kilimo-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/kilimo-mcp"
LABEL org.opencontainers.image.description="kilimo-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir kilimo-mcp

CMD ["kilimo-mcp"]
