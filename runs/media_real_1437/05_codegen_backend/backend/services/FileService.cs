using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class FileService
{
    private readonly InMemoryStore _store;

    public FileService(InMemoryStore store)
    {
        _store = store;
    }

    public (GetUploadUrlResponse? Response, string? Error, int? StatusCode) GetUploadUrl(GetUploadUrlRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.MimeType))
        {
            return (null, "MIME type is required.", 400);
        }

        if (request.SizeBytes <= 0)
        {
            return (null, "File size must be positive.", 400);
        }

        var isReference = request.IsReference ?? false;
        var fileId = Guid.NewGuid().ToString();
        var s3Key = $"{(isReference ? "reference" : "media")}/{fileId}";
        var expiresAt = DateTime.UtcNow.AddHours(1);

        if (isReference)
        {
            var referenceFile = new ReferenceFile
            {
                Id = fileId,
                S3Key = s3Key,
                MimeType = request.MimeType
            };
            _store.AddReferenceFile(referenceFile);
        }
        else
        {
            var mediaFile = new MediaFile
            {
                Id = fileId,
                S3Key = s3Key,
                MimeType = request.MimeType,
                SizeBytes = request.SizeBytes
            };
            _store.AddMediaFile(mediaFile);
        }

        return (new GetUploadUrlResponse
        {
            FileId = fileId,
            UploadUrl = $"https://s3.amazonaws.com/bucket/{s3Key}?X-Amz-Expires=3600&X-Amz-Signature=placeholder",
            S3Key = s3Key,
            ExpiresAt = expiresAt
        }, null, null);
    }

    public (ConfirmFileUploadResponse? Response, string? Error, int? StatusCode) ConfirmFileUpload(string id)
    {
        var referenceFile = _store.GetReferenceFile(id);
        if (referenceFile != null)
        {
            return (new ConfirmFileUploadResponse
            {
                FileId = id,
                Status = "confirmed"
            }, null, null);
        }

        var mediaFile = _store.GetMediaFile(id);
        if (mediaFile != null)
        {
            return (new ConfirmFileUploadResponse
            {
                FileId = id,
                Status = "confirmed"
            }, null, null);
        }

        return (null, "File not found.", 404);
    }
}
