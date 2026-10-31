using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;
using MediaProcessingApi.Storage;

namespace MediaProcessingApi.Services;

public class ApplicationService : IApplicationService
{
    private readonly InMemoryStorage _storage;

    public ApplicationService(InMemoryStorage storage)
    {
        _storage = storage;
    }

    public async Task<CreateApplicationResponse> CreateApplicationAsync(CreateApplicationRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Type) ||
            (request.Type != "photo" && request.Type != "video"))
        {
            throw new BadRequestException("Invalid application type.");
        }

        if (string.IsNullOrWhiteSpace(request.ReferenceTemplateId))
        {
            throw new BadRequestException("Reference template ID is required.");
        }

        if (string.IsNullOrWhiteSpace(request.MediaS3Key))
        {
            throw new BadRequestException("Media S3 key is required.");
        }

        var templateExists = _storage.ReferenceTemplates.Any(t => t.Id == request.ReferenceTemplateId);
        if (!templateExists)
        {
            throw new BadRequestException("Reference template not found.");
        }

        var application = new Application
        {
            Id = Guid.NewGuid().ToString(),
            Type = request.Type,
            Status = "pending",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = null
        };

        _storage.Applications.Add(application);

        var mediaFile = new MediaFile
        {
            Id = Guid.NewGuid().ToString(),
            ApplicationId = application.Id,
            S3Key = request.MediaS3Key,
            FileType = request.Type == "photo" ? "source_photo" : "source_video",
            DurationSeconds = null,
            CreatedAt = DateTime.UtcNow
        };

        _storage.MediaFiles.Add(mediaFile);

        return new CreateApplicationResponse
        {
            ApplicationId = application.Id,
            Status = application.Status
        };
    }

    public async Task<GetApplicationResponse> GetApplicationAsync(string applicationId)
    {
        var application = _storage.Applications.FirstOrDefault(a => a.Id == applicationId);
        if (application == null)
        {
            throw new NotFoundException("Application not found.");
        }

        var photoResult = _storage.PhotoAnalysisResults.FirstOrDefault(p => p.ApplicationId == applicationId);
        var videoResult = _storage.VideoAnalysisResults.FirstOrDefault(v => v.ApplicationId == applicationId);

        return new GetApplicationResponse
        {
            ApplicationId = application.Id,
            Status = application.Status,
            PhotoResult = photoResult != null ? new
            {
                photoResult.Id,
                photoResult.SimilarityScore,
                photoResult.Status,
                photoResult.QualityMetrics,
                photoResult.CreatedAt
            } : null,
            VideoResult = videoResult != null ? new
            {
                videoResult.Id,
                videoResult.CreatedAt,
                Segments = _storage.VideoSegments.Where(s => s.AnalysisId == videoResult.Id).Select(s => new
                {
                    s.Id,
                    s.StartTime,
                    s.EndTime,
                    s.Confidence
                }).ToList()
            } : null
        };
    }

    public async Task<TriggerProcessingResponse> TriggerProcessingAsync(string applicationId)
    {
        var application = _storage.Applications.FirstOrDefault(a => a.Id == applicationId);
        if (application == null)
        {
            throw new NotFoundException("Application not found.");
        }

        if (application.Status == "processing")
        {
            throw new ConflictException("Application is already being processed.");
        }

        var jobType = application.Type == "photo" ? "photo_analysis" : "video_analysis";

        var job = new ProcessingJob
        {
            Id = Guid.NewGuid().ToString(),
            ApplicationId = application.Id,
            JobType = jobType,
            Status = "queued",
            StartedAt = null,
            CompletedAt = null,
            ErrorMessage = null
        };

        _storage.ProcessingJobs.Add(job);

        application.Status = "processing";
        application.UpdatedAt = DateTime.UtcNow;

        return new TriggerProcessingResponse
        {
            JobId = job.Id,
            Status = job.Status
        };
    }

    public async Task<GetApplicationResultsResponse> GetApplicationResultsAsync(string applicationId)
    {
        var application = _storage.Applications.FirstOrDefault(a => a.Id == applicationId);
        if (application == null)
        {
            throw new NotFoundException("Application not found.");
        }

        var photoAnalysis = _storage.PhotoAnalysisResults.FirstOrDefault(p => p.ApplicationId == applicationId);
        var videoAnalysis = _storage.VideoAnalysisResults.FirstOrDefault(v => v.ApplicationId == applicationId);
        var resultFiles = _storage.MediaFiles
            .Where(m => m.ApplicationId == applicationId && (m.FileType == "result_photo" || m.FileType == "result_video"))
            .Select(m => new
            {
                m.Id,
                m.S3Key,
                m.FileType,
                m.DurationSeconds,
                m.CreatedAt
            })
            .ToList();

        return new GetApplicationResultsResponse
        {
            PhotoAnalysis = photoAnalysis != null ? new
            {
                photoAnalysis.Id,
                photoAnalysis.SimilarityScore,
                photoAnalysis.Status,
                photoAnalysis.QualityMetrics,
                photoAnalysis.CreatedAt
            } : null,
            VideoAnalysis = videoAnalysis != null ? new
            {
                videoAnalysis.Id,
                videoAnalysis.CreatedAt,
                Segments = _storage.VideoSegments.Where(s => s.AnalysisId == videoAnalysis.Id).Select(s => new
                {
                    s.Id,
                    s.StartTime,
                    s.EndTime,
                    s.Confidence
                }).ToList()
            } : null,
            ResultFiles = resultFiles
        };
    }
}
