# User Guide

## FR-001: Photo Verification
1. Open app (Android/PWA).
2. Select photo and reference template (JPEG/PNG).
3. Start processing.
4. Result: similarity % and status (Matches/Does not match/Low quality).
5. On success, photo is linked to request.

## FR-002: Video Analysis
1. Upload video (150-300s) and reference template.
2. System detects creative timestamps (start_time, end_time).
3. Report with timestamps is generated.

## FR-003: Video Cutting
1. System cuts 15s clip using detected timestamps.
2. Output: MP4 (H.264), accuracy ±0.1s.
3. Clip is linked to request.

## FR-004: Storage & Integration
1. Final file saved to S3.
2. Status 'Completed' + file link sent via Kafka and REST API.