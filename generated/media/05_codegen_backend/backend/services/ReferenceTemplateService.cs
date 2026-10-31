using MediaProcessingApi.Dtos;
using MediaProcessingApi.Entities;
using MediaProcessingApi.Storage;

namespace MediaProcessingApi.Services;

public class ReferenceTemplateService : IReferenceTemplateService
{
    private readonly InMemoryStorage _storage;

    public ReferenceTemplateService(InMemoryStorage storage)
    {
        _storage = storage;
    }

    public async Task<UploadReferenceTemplateResponse> UploadReferenceTemplateAsync(UploadReferenceTemplateRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.S3Key))
        {
            throw new BadRequestException("S3 key is required.");
        }

        if (string.IsNullOrWhiteSpace(request.Format) ||
            (request.Format != "JPEG" && request.Format != "PNG"))
        {
            throw new BadRequestException("Invalid format. Must be JPEG or PNG.");
        }

        var template = new ReferenceTemplate
        {
            Id = Guid.NewGuid().ToString(),
            S3Key = request.S3Key,
            Format = request.Format,
            CreatedAt = DateTime.UtcNow
        };

        _storage.ReferenceTemplates.Add(template);

        return new UploadReferenceTemplateResponse
        {
            TemplateId = template.Id
        };
    }

    public async Task<GetReferenceTemplateResponse> GetReferenceTemplateAsync(string templateId)
    {
        var template = _storage.ReferenceTemplates.FirstOrDefault(t => t.Id == templateId);
        if (template == null)
        {
            throw new NotFoundException("Reference template not found.");
        }

        return new GetReferenceTemplateResponse
        {
            TemplateId = template.Id,
            S3Key = template.S3Key,
            Format = template.Format
        };
    }
}
