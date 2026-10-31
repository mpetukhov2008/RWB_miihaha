namespace MediaProcessingApi.Dtos;

public class PhotoAnalysisResultResponse
{
    public string ApplicationId { get; set; } = string.Empty;
    public double SimilarityScore { get; set; }
    public string QualityStatus { get; set; } = string.Empty;
    public string MatchStatus { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
