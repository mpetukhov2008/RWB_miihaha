namespace MediaProcessingApi.Dtos;

public class CreateApplicationRequest
{
    public string Type { get; set; } = string.Empty;
    public string ReferenceTemplateId { get; set; } = string.Empty;
    public string MediaS3Key { get; set; } = string.Empty;
}
