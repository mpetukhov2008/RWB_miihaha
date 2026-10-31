namespace MediaProcessingApi.Entities;

public class MediaFile
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string S3Key { get; set; } = string.Empty;
    public string MimeType { get; set; } = string.Empty;
    public long SizeBytes { get; set; }
    public double? DurationSeconds { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
