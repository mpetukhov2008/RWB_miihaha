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

    public (CreateApplicationResponse? response, string? error, int? statusCode) CreateApplication(CreateApplicationRequest request)
    {
        if (request.Type != "photo" && request.Type != "video")
        {
            return (null, "Invalid application type.", 400);
        }

        if (string.IsNullOrWhiteSpace(request.ReferenceFileId) || string.IsNullOrWhiteSpace(request.SourceFileId))
        {
            return (null, "Reference file ID and source file ID are required.", 400);
        }

        var referenceFile = _store.GetFile(request.ReferenceFileId);
        if (referenceFile == null)
        {
            return (null, "Reference file not found.", 400);
        }

        var sourceFile = _store.GetFile(request.SourceFileId);
        if (sourceFile == null)
        {
            return (null, "Source file not found.", 400);
        }

        if (referenceFile.FileRole != "reference")
        {
            return (null, "Reference file must have role 'reference'.", 400);
        }

        if (sourceFile.FileRole != "source")
        {
            return (null, "Source file must have role 'source'.", 400);
        }

        if (request.Type == "photo" && sourceFile.FileType == "mp4")
        {
            return (null, "Photo application requires a photo source file.", 400);
        }

        if (request.Type == "video" && sourceFile.FileType != "mp4")
        {
            return (null, "Video application requires an mp4 source file.", 400);
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
            CreatedAt = application.CreatedAt.ToString("o")
        }, null, null);
    }

    public (GetApplicationResponse? response, string? error, int? statusCode) GetApplication(string id)
    {
        var application = _store.GetApplication(id);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        var segments = _store.GetSegmentsByApplicationId(id);
        var resultFileIds = new List<string>();
        if (!string.IsNullOrEmpty(application.ResultFileId))
        {
            resultFileIds.Add(application.ResultFileId);
        }
        foreach (var segment in segments)
        {
            if (!string.IsNullOrEmpty(segment.ResultFileId))
            {
                resultFileIds.Add(segment.ResultFileId);
            }
        }

        return (new GetApplicationResponse
        {
            Id = application.Id,
            Type = application.Type,
            Status = application.Status,
            SimilarityScore = application.SimilarityScore,
            VerificationStatus = application.VerificationStatus,
            ResultFileIds = resultFileIds,
            Segments = segments.Select(s => new SegmentDto
            {
                Id = s.Id,
                StartTime = s.StartTime,
                EndTime = s.EndTime,
                Confidence = s.Confidence,
                ResultFileId = s.ResultFileId
            }).ToList(),
            CreatedAt = application.CreatedAt.ToString("o"),
            UpdatedAt = application.UpdatedAt.ToString("o")
        }, null, null);
    }

    public (TriggerProcessingResponse? response, string? error, int? statusCode) TriggerProcessing(string id)
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

        if (_store.HasActiveJobForApplication(id))
        {
            return (null, "An active processing job already exists for this application.", 409);
        }

        var jobType = application.Type == "photo" ? "photo_verification" : "video_detection";
        var job = new ProcessingJob
        {
            ApplicationId = application.Id,
            JobType = jobType,
            Status = "queued"
        };

        _store.AddJob(job);

        application.Status = "processing";
        application.UpdatedAt = DateTime.UtcNow;
        _store.UpdateApplication(application);

        return (new TriggerProcessingResponse
        {
            ApplicationId = application.Id,
            JobId = job.Id,
            Status = application.Status
        }, null, null);
    }

    public (GetVideoSegmentsResponse? response, string? error, int? statusCode) GetVideoSegments(string id)
    {
        var application = _store.GetApplication(id);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        var segments = _store.GetSegmentsByApplicationId(id);

        return (new GetVideoSegmentsResponse
        {
            ApplicationId = application.Id,
            Segments = segments.Select(s => new SegmentDto
            {
                Id = s.Id,
                StartTime = s.StartTime,
                EndTime = s.EndTime,
                Confidence = s.Confidence,
                ResultFileId = s.ResultFileId
            }).ToList()
        }, null, null);
    }
}
