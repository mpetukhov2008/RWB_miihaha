using MediaProcessingApi.Dtos;

namespace MediaProcessingApi.Services;

public interface IWebhookService
{
    Task<ReceiveStatusWebhookResponse> ReceiveStatusWebhookAsync(ReceiveStatusWebhookRequest request);
}
