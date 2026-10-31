# Known Limitations

## Assumptions
- Target ad clip duration is fixed at 15 seconds.
- Employees upload files in areas with stable internet for heavy video transfer to S3/backend.

## Security & Performance
- Glare, overexposure, defocus, or sharp shooting angles may reduce recognition accuracy below 95%.
- Processing 300s videos with parallel loads may exceed the 20-minute limit.
- Differences between static template and dynamic video may complicate start/end time detection.
- Secure transfer of media data and statuses is required.
- Integration with existing mobile app (Android/PWA) is supported.