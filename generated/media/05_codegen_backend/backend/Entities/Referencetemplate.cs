namespace MediaProcessingApi.Entities;

public class ReferenceTemplate
{
    public string Id { get; set; } = string.Empty;
    public string S3Key { get; set; } = string.Empty;
    public string Format { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
