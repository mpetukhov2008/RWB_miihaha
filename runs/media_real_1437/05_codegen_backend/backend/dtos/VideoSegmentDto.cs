namespace MediaProcessingApi.Dtos;

public class VideoSegmentDto
{
    public string Id { get; set; } = string.Empty;
    public double StartTime { get; set; }
    public double EndTime { get; set; }
    public string? ResultFileId { get; set; }
}
