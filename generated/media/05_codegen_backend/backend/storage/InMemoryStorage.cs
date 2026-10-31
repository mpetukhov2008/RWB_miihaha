using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Storage;

public class InMemoryStorage
{
    public List<Application> Applications { get; } = new();
    public List<ReferenceTemplate> ReferenceTemplates { get; } = new();
    public List<MediaFile> MediaFiles { get; } = new();
    public List<PhotoAnalysisResult> PhotoAnalysisResults { get; } = new();
    public List<VideoAnalysisResult> VideoAnalysisResults { get; } = new();
    public List<VideoSegment> VideoSegments { get; } = new();
    public List<ProcessingJob> ProcessingJobs { get; } = new();
}
