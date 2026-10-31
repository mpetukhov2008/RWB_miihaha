namespace MediaProcessingApi.Entities;

public class VideoSegment
{
    public string Id { get; set; } = string.Empty;
    public string AnalysisId { get; set; } = string.Empty;
    public double StartTime { get; set; }
    public double EndTime { get; set; }
    public double? Confidence { get; set; }
}
