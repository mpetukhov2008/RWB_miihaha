using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class PhotoAnalysisService
{
    private readonly InMemoryStore _store;

    public PhotoAnalysisService(InMemoryStore store)
    {
        _store = store;
    }

    public (PhotoAnalysisResultResponse? Response, string? Error, int? StatusCode) GetPhotoAnalysisResult(string applicationId)
    {
        var application = _store.GetApplication(applicationId);
        if (application == null)
        {
            return (null, "Application not found.", 404);
        }

        if (application.Type != "photo")
        {
            return (null, "Application is not a photo application.", 404);
        }

        var result = _store.GetPhotoAnalysisResult(applicationId);
        if (result == null)
        {
            return (null, "Photo analysis result not found.", 404);
        }

        return (new PhotoAnalysisResultResponse
        {
            ApplicationId = result.ApplicationId,
            SimilarityScore = result.SimilarityScore,
            QualityStatus = result.QualityStatus,
            MatchStatus = result.MatchStatus,
            CreatedAt = result.CreatedAt
        }, null, null);
    }
}
