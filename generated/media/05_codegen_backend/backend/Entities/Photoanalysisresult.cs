namespace MediaProcessingApi.Entities;

public class PhotoAnalysisResult
{
    public string Id { get; set; } = string.Empty;
    public string ApplicationId { get; set; } = string.Empty;
    public double SimilarityScore { get; set; }
    public string Status { get; set; } = string.Empty;
    public object? QualityMetrics { get; set; }
    public DateTime CreatedAt { get; set; }
}
