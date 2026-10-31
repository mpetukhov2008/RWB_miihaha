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

    public (GetUploadUrlResponse? response, string? error, int? statusCode) GetUploadUrl(GetUploadUrlRequest request)
    {
        if (request.FileType != "jpeg" && request.FileType != "png" && request.FileType != "mp4")
        {
            return (null, "Invalid file type.", 400);
        }

        if (request.FileRole != "source" && request.FileRole != "reference")
        {
            return (null, "Invalid file role.", 400);
        }

        if (request.SizeBytes <= 0)
        {
            return (null, "File size must be positive.", 400);
        }

        var fileId = Guid.NewGuid().ToString();
        var s3Key = $"uploads/{request.FileRole}/{fileId}.{request.FileType}";
        var expiresAt = DateTime.UtcNow.AddHours(1);

        var file = new MediaFile
        {
            Id = fileId,
            S3Key = s3Key,
            FileType = request.FileType,
            FileRole = request.FileRole,
            SizeBytes = request.SizeBytes,
            Status = "pending"
        };

        _store.AddFile(file);

        return (new GetUploadUrlResponse
        {
            FileId = fileId,
            UploadUrl = $"https://s3.amazonaws.com/bucket/{s3Key}?X-Amz-Expires=3600&X-Amz-Signature=mock",
            S3Key = s3Key,
            ExpiresAt = expiresAt.ToString("o")
        }, null, null);
    }

    public (ConfirmFileUploadResponse? response, string? error, int? statusCode) ConfirmFileUpload(string id)
    {
        var file = _store.GetFile(id);
        if (file == null)
        {
            return (null, "File not found.", 404);
        }

        file.Status = "confirmed";
        _store.UpdateFile(file);

        return (new ConfirmFileUploadResponse
        {
            FileId = file.Id,
            Status = file.Status
        }, null, null);
    }

    public (GetDownloadUrlResponse? response, string? error, int? statusCode) GetDownloadUrl(string id)
    {
        var file = _store.GetFile(id);
        if (file == null)
        {
            return (null, "File not found.", 404);
        }

        var expiresAt = DateTime.UtcNow.AddHours(1);

        return (new GetDownloadUrlResponse
        {
            FileId = file.Id,
            DownloadUrl = $"https://s3.amazonaws.com/bucket/{file.S3Key}?X-Amz-Expires=3600&X-Amz-Signature=mock",
            ExpiresAt = expiresAt.ToString("o")
        }, null, null);
    }
}
