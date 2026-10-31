namespace MediaProcessingApi.Dtos;

public class GetUploadUrlResponse
{
    public string FileId { get; set; } = string.Empty;
    public string UploadUrl { get; set; } = string.Empty;
    public string S3Key { get; set; } = string.Empty;
    public string ExpiresAt { get; set; } = string.Empty;
}
