namespace MediaProcessingApi.Dtos;

public class GetApplicationResponse
{
    public string Id { get; set; } = string.Empty;
    public string Type { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public double? SimilarityScore { get; set; }
    public string? VerificationStatus { get; set; }
    public List<string> ResultFileIds { get; set; } = new();
    public List<SegmentDto> Segments { get; set; } = new();
    public string CreatedAt { get; set; } = string.Empty;
    public string UpdatedAt { get; set; } = string.Empty;
}
