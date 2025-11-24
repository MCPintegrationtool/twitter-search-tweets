FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
#COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "mcp[cli]" fastmcp requests

# Optional: install uv tool if you want to run server via uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy the application code
COPY ./server.py /app/server.py

# Create entrypoint.sh
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'set -e' >> /app/entrypoint.sh && \
    echo 'if [ -z "$BEARER_TOKEN" ]; then' >> /app/entrypoint.sh && \
    echo '  echo "ERROR: BEARER_TOKEN is not set"' >> /app/entrypoint.sh && \
    echo '  exit 1' >> /app/entrypoint.sh && \
    echo 'fi' >> /app/entrypoint.sh && \
    echo 'echo "Starting Twitter MCP Server"' >> /app/entrypoint.sh && \
    echo 'if [ "$USE_UV" = "1" ]; then' >> /app/entrypoint.sh && \
    echo '  exec uv run server.py' >> /app/entrypoint.sh && \
    echo 'else' >> /app/entrypoint.sh && \
    echo '  exec python /app/server.py' >> /app/entrypoint.sh && \
    echo 'fi' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Create non-root user (optional, safer)
RUN useradd -m mcp && chown -R mcp /app
USER mcp
EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]
