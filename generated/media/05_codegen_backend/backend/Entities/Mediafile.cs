namespace MediaProcessingApi.Entities;

public class MediaFile
{
    public string Id { get; set; } = string.Empty;
    public string ApplicationId { get; set; } = string.Empty;
    public string S3Key { get; set; } = string.Empty;
    public string FileType { get; set; } = string.Empty;
    public double? DurationSeconds { get; set; }
    public DateTime CreatedAt { get; set; }
}
