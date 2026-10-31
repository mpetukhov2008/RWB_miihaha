# Run Instructions

## Docker Compose
```bash
docker compose up -d
```

## Services
- backend: .NET API
- vision: OpenCV/PyTorch CV service
- ffmpeg: video processing
- kafka: event streaming
- s3: object storage (MinIO for local)

## Verify
```bash
curl http://localhost:8080/health
```

## Stop
```bash
docker compose down
```