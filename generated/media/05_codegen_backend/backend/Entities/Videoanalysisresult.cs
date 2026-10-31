namespace MediaProcessingApi.Entities;

public class VideoAnalysisResult
{
    public string Id { get; set; } = string.Empty;
    public string ApplicationId { get; set; } = string.Empty;
    public List<VideoSegment> Segments { get; set; } = new();
    public DateTime CreatedAt { get; set; }
}
