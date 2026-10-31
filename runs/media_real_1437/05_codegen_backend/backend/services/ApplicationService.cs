using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class ApplicationService
{
    private readonly InMemoryStore _store;

    public ApplicationService(InMemoryStore store)
    {
        _store = store;
    }

    public (CreateApplicationResponse? Response, string? Error, int? StatusCode) CreateApplication(CreateApplicationRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Type) || (request.Type != "photo" && request.Type != "video"))
        {
            return (null, "Invalid application type. Must be 'photo' or 'video'.", 400);
        }

        if (string.IsNullOrWhiteSpace(request.ReferenceFileId))
        {
            return (null, "Reference file ID is required.", 400);
        }

        if (string.IsNullOrWhiteSpace(request.SourceFileId))
        {
            return (null, "Source file ID is required.", 400);
        }

        var referenceFile = _store.GetReferenceFile(request.ReferenceFileId);
        if (referenceFile == null)
        {
            return (null, "Reference file not found.", 404);
        }

        var sourceFile = _store.GetMediaFile(request.SourceFileId);
        if (sourceFile == null)
        {
            return (null, "Source file not found.", 404);
        }

        var application = new Application
        {
            Type = request.Type,
            ReferenceFileId = request.ReferenceFileId,
            SourceFileId = request.SourceFileId,
            Status = "pending"
        };

        _store.AddApplication(application);

        return (new CreateApplicationResponse
        {
            Id = application.Id,
            Status = application.Status,
            CreatedAt = application.CreatedAt
        }, null, null);
    }

    public (GetApplicationResponse? Response, string? Error, int? StatusCode) GetApplication(string id)
    {
        var application = _store.GetApplication(id);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        return (new GetApplicationResponse
        {
            Id = application.Id,
            Type = application.Type,
            Status = application.Status,
            ReferenceFileId = application.ReferenceFileId,
            SourceFileId = application.SourceFileId,
            ResultFileId = application.ResultFileId,
            CreatedAt = application.CreatedAt,
            UpdatedAt = application.UpdatedAt
        }, null, null);
    }

    public (TriggerProcessingResponse? Response, string? Error, int? StatusCode) TriggerProcessing(string id)
    {
        var application = _store.GetApplication(id);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        if (application.Status == "processing")
        {
            return (null, "Application is already being processed.", 409);
        }

        if (application.Status == "completed")
        {
            return (null, "Application has already been completed.", 409);
        }

        application.Status = "processing";
        _store.UpdateApplication(application);

        return (new TriggerProcessingResponse
        {
            ApplicationId = application.Id,
            Status = application.Status,
            Message = "Processing started."
        }, null, null);
    }
}
