FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY pipeline ./pipeline
COPY schemas ./schemas
COPY cases ./cases
COPY templates ./templates
COPY run_pipeline.sh ./
RUN chmod +x run_pipeline.sh

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["./run_pipeline.sh"]
CMD ["cases/parking/requirements.md"]
