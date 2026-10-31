namespace MediaProcessingApi.Entities;

public class Application
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Type { get; set; } = string.Empty;
    public string Status { get; set; } = "pending";
    public string ReferenceFileId { get; set; } = string.Empty;
    public string SourceFileId { get; set; } = string.Empty;
    public string? ResultFileId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}
