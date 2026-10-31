namespace MediaProcessingApi.Dtos;

public class GetReferenceTemplateResponse
{
    public string TemplateId { get; set; } = string.Empty;
    public string S3Key { get; set; } = string.Empty;
    public string Format { get; set; } = string.Empty;
}
