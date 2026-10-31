namespace MediaProcessingApi.Dtos;

public class GetApplicationResponse
{
    public string Id { get; set; } = string.Empty;
    public string Type { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string ReferenceFileId { get; set; } = string.Empty;
    public string SourceFileId { get; set; } = string.Empty;
    public string? ResultFileId { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
