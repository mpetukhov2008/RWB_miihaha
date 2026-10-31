namespace MediaProcessingApi.Entities;

public class ReferenceFile
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string S3Key { get; set; } = string.Empty;
    public string MimeType { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
