namespace MediaProcessingApi.Dtos;

public class VideoAnalysisResultResponse
{
    public string ApplicationId { get; set; } = string.Empty;
    public List<VideoSegmentDto> Segments { get; set; } = new();
    public DateTime CreatedAt { get; set; }
}
