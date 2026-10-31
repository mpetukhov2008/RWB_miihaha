using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;
using MediaProcessingApi.Storage;

namespace MediaProcessingApi.Services;

public class WebhookService : IWebhookService
{
    private readonly InMemoryStorage _storage;

    public WebhookService(InMemoryStorage storage)
    {
        _storage = storage;
    }

    public async Task<ReceiveStatusWebhookResponse> ReceiveStatusWebhookAsync(ReceiveStatusWebhookRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.ApplicationId))
        {
            throw new BadRequestException("Application ID is required.");
        }

        if (string.IsNullOrWhiteSpace(request.Status))
        {
            throw new BadRequestException("Status is required.");
        }

        var application = _storage.Applications.FirstOrDefault(a => a.Id == request.ApplicationId);
        if (application == null)
        {
            throw new BadRequestException("Application not found.");
        }

        application.Status = request.Status;
        application.UpdatedAt = DateTime.UtcNow;

        if (!string.IsNullOrWhiteSpace(request.ResultS3Key))
        {
            var resultFileType = application.Type == "photo" ? "result_photo" : "result_video";
            var resultFile = new MediaFile
            {
                Id = Guid.NewGuid().ToString(),
                ApplicationId = application.Id,
                S3Key = request.ResultS3Key,
                FileType = resultFileType,
                DurationSeconds = null,
                CreatedAt = DateTime.UtcNow
            };

            _storage.MediaFiles.Add(resultFile);
        }

        return new ReceiveStatusWebhookResponse
        {
            Received = true
        };
    }
}
