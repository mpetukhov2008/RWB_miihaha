namespace MediaProcessingApi.Dtos;

public class GetApplicationResponse
{
    public string ApplicationId { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public object? PhotoResult { get; set; }
    public object? VideoResult { get; set; }
}
