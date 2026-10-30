FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY pipeline ./pipeline
COPY prompts ./prompts
COPY examples ./examples

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["pipeline"]
CMD ["--help"]