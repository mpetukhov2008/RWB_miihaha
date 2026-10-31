using MediaProcessingApi.Dtos;

namespace MediaProcessingApi.Services;

public interface IApplicationService
{
    Task<CreateApplicationResponse> CreateApplicationAsync(CreateApplicationRequest request);
    Task<GetApplicationResponse> GetApplicationAsync(string applicationId);
    Task<TriggerProcessingResponse> TriggerProcessingAsync(string applicationId);
    Task<GetApplicationResultsResponse> GetApplicationResultsAsync(string applicationId);
}
