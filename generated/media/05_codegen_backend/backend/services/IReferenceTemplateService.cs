using MediaProcessingApi.Dtos;

namespace MediaProcessingApi.Services;

public interface IReferenceTemplateService
{
    Task<UploadReferenceTemplateResponse> UploadReferenceTemplateAsync(UploadReferenceTemplateRequest request);
    Task<GetReferenceTemplateResponse> GetReferenceTemplateAsync(string templateId);
}
