namespace MediaProcessingApi.Entities;

public class PhotoAnalysisResult
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string ApplicationId { get; set; } = string.Empty;
    public double SimilarityScore { get; set; }
    public string QualityStatus { get; set; } = string.Empty;
    public string MatchStatus { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
