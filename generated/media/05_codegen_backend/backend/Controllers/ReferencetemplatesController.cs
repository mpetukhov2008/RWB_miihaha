using Microsoft.AspNetCore.Mvc;
using MediaProcessingApi.Dtos;
using MediaProcessingApi.Services;

namespace MediaProcessingApi.Controllers;

[ApiController]
[Route("reference-templates")]
[Authorize]
public class ReferenceTemplatesController : ControllerBase
{
    private readonly IReferenceTemplateService _referenceTemplateService;

    public ReferenceTemplatesController(IReferenceTemplateService referenceTemplateService)
    {
        _referenceTemplateService = referenceTemplateService;
    }

    [HttpPost]
    [ProducesResponseType(typeof(UploadReferenceTemplateResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> UploadReferenceTemplate([FromBody] UploadReferenceTemplateRequest request)
    {
        var response = await _referenceTemplateService.UploadReferenceTemplateAsync(request);
        return Created($"/reference-templates/{response.TemplateId}", response);
    }

    [HttpGet("{templateId}")]
    [ProducesResponseType(typeof(GetReferenceTemplateResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetReferenceTemplate(string templateId)
    {
        var response = await _referenceTemplateService.GetReferenceTemplateAsync(templateId);
        return Ok(response);
    }
}
