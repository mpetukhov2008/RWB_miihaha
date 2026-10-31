namespace MediaProcessingApi.Dtos;

public class ReceiveStatusWebhookRequest
{
    public string ApplicationId { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string? ResultS3Key { get; set; }
}
