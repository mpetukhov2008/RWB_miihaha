namespace MediaProcessingApi.Dtos;

public class GetUploadUrlRequest
{
    public string MimeType { get; set; } = string.Empty;
    public long SizeBytes { get; set; }
    public bool? IsReference { get; set; }
}
