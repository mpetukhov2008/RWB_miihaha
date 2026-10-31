# Product Description

Automated system for recognizing, quality-checking, and verifying photo reports against reference templates, detecting and cutting 15-second ad clips from 150-300s video streams, and storing results in S3 with integration to adjacent systems via Kafka/REST API.

## Goals
- Automate photo report recognition and verification
- Automate ad clip detection and cutting from video
- Automatically store media files in S3 and link results to requests

## Roles
- Technical service employee: captures media, starts processing
- Adjacent system: receives files in S3 and statuses via Kafka/REST