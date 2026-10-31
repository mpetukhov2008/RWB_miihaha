namespace MediaProcessingApi.Dtos;

public class CreateApplicationRequest
{
    public string Type { get; set; } = string.Empty;
    public string ReferenceFileId { get; set; } = string.Empty;
    public string SourceFileId { get; set; } = string.Empty;
}
