namespace MediaProcessingApi.Dtos;

public class UploadReferenceTemplateRequest
{
    public string S3Key { get; set; } = string.Empty;
    public string Format { get; set; } = string.Empty;
}
