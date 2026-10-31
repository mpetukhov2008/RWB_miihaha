namespace MediaProcessingApi.Dtos;

public class GetDownloadUrlResponse
{
    public string FileId { get; set; } = string.Empty;
    public string DownloadUrl { get; set; } = string.Empty;
    public string ExpiresAt { get; set; } = string.Empty;
}
