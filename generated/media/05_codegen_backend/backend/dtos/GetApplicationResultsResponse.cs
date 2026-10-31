namespace MediaProcessingApi.Dtos;

public class GetApplicationResultsResponse
{
    public object? PhotoAnalysis { get; set; }
    public object? VideoAnalysis { get; set; }
    public List<object> ResultFiles { get; set; } = new();
}
