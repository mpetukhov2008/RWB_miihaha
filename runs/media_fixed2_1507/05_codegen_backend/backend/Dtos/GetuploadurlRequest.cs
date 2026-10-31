namespace MediaProcessingApi.Dtos;

public class GetUploadUrlRequest
{
    public string FileType { get; set; } = string.Empty;
    public string FileRole { get; set; } = string.Empty;
    public long SizeBytes { get; set; }
}
