# Developer Guide

## Architecture
- **Mobile**: Kotlin (Android) / Angular (PWA)
- **Backend**: C# / .NET
- **CV**: OpenCV, PyTorch/TensorFlow
- **Video**: FFmpeg
- **Storage**: S3, Kafka, REST API

## Flow
1. Mobile uploads media + reference to backend.
2. Backend queues job, calls CV service.
3. CV detects creative, returns timestamps/similarity.
4. FFmpeg cuts video (if applicable).
5. Result saved to S3.
6. Kafka event + REST callback sent.

## Key Components
- PhotoVerifier: quality check + template matching
- VideoDetector: frame analysis for timestamps
- VideoCutter: FFmpeg-based 15s extraction
- IntegrationService: S3 upload + Kafka/REST notifications