using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class VideoAnalysisService
{
    private readonly InMemoryStore _store;

    public VideoAnalysisService(InMemoryStore store)
    {
        _store = store;
    }

    public (VideoAnalysisResultResponse? Response, string? Error, int? StatusCode) GetVideoAnalysisResult(string applicationId)
    {
        var application = _store.GetApplication(applicationId);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        if (application.Type != "video")
        {
            return (null, "Application is not a video application.", 404);
        }

        var result = _store.GetVideoAnalysisResult(applicationId);
        if (result == null)
        {
            return (null, "Video analysis result not found.", 404);
        }

        return (new VideoAnalysisResultResponse
        {
            ApplicationId = result.ApplicationId,
            Segments = result.Segments.Select(s => new VideoSegmentDto
            {
                Id = s.Id,
                StartTime = s.StartTime,
                EndTime = s.EndTime,
                ResultFileId = s.ResultFileId
            }).ToList(),
            CreatedAt = result.CreatedAt
        }, null, null);
    }
}
