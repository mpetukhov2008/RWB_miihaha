namespace MediaProcessingApi.Dtos;

public class GetVideoSegmentsResponse
{
    public string ApplicationId { get; set; } = string.Empty;
    public List<SegmentDto> Segments { get; set; } = new();
}
