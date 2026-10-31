namespace MediaProcessingApi.Dtos;

public class SegmentDto
{
    public string? Id { get; set; }
    public double StartTime { get; set; }
    public double EndTime { get; set; }
    public double? Confidence { get; set; }
    public string? ResultFileId { get; set; }
}
