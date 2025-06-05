FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
RUN uv sync --locked

EXPOSE 8080

# Run the application.
CMD ["sh", "-c", "cd /app && uv run python server.py --host 0.0.0.0 --port ${PORT:-8080}"]
