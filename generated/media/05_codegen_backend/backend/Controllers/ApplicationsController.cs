using Microsoft.AspNetCore.Mvc;
using MediaProcessingApi.Dtos;
using MediaProcessingApi.Services;

namespace MediaProcessingApi.Controllers;

[ApiController]
[Route("applications")]
[Authorize]
public class ApplicationsController : ControllerBase
{
    private readonly IApplicationService _applicationService;

    public ApplicationsController(IApplicationService applicationService)
    {
        _applicationService = applicationService;
    }

    [HttpPost]
    [ProducesResponseType(typeof(CreateApplicationResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status409Conflict)]
    public async Task<IActionResult> CreateApplication([FromBody] CreateApplicationRequest request)
    {
        var response = await _applicationService.CreateApplicationAsync(request);
        return Created($"/applications/{response.ApplicationId}", response);
    }

    [HttpGet("{applicationId}")]
    [ProducesResponseType(typeof(GetApplicationResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetApplication(string applicationId)
    {
        var response = await _applicationService.GetApplicationAsync(applicationId);
        return Ok(response);
    }

    [HttpPost("{applicationId}/process")]
    [ProducesResponseType(typeof(TriggerProcessingResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status409Conflict)]
    public async Task<IActionResult> TriggerProcessing(string applicationId)
    {
        var response = await _applicationService.TriggerProcessingAsync(applicationId);
        return Ok(response);
    }

    [HttpGet("{applicationId}/results")]
    [ProducesResponseType(typeof(GetApplicationResultsResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetApplicationResults(string applicationId)
    {
        var response = await _applicationService.GetApplicationResultsAsync(applicationId);
        return Ok(response);
    }
}
