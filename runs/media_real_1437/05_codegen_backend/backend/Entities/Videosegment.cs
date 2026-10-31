namespace MediaProcessingApi.Entities;

public class VideoSegment
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string VideoAnalysisId { get; set; } = string.Empty;
    public double StartTime { get; set; }
    public double EndTime { get; set; }
    public string? ResultFileId { get; set; }
}
