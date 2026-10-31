using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MediaProcessingApi.Dtos;
using MediaProcessingApi.Services;

namespace MediaProcessingApi.Controllers;

[ApiController]
[Route("applications")]
[Authorize]
public class ApplicationsController : ControllerBase
{
    private readonly ApplicationService _applicationService;

    public ApplicationsController(ApplicationService applicationService)
    {
        _applicationService = applicationService;
    }

    [HttpPost]
    public IActionResult CreateApplication([FromBody] CreateApplicationRequest request)
    {
        var (response, error, statusCode) = _applicationService.CreateApplication(request);
        if (error != null)
        {
            return Problem("Ошибка обработки");
        }

        return CreatedAtAction(nameof(GetApplication), new { id = response.Id }, response);
    }

    [HttpGet("{id}")]
    public IActionResult GetApplication(string id)
    {
        var (response, error, statusCode) = _applicationService.GetApplication(id);
        if (error != null)
        {
            return Problem("Ошибка обработки");
        }

        return Ok(response);
    }

    [HttpPost("{id}/process")]
    public IActionResult TriggerProcessing(string id)
    {
        var (response, error, statusCode) = _applicationService.TriggerProcessing(id);
        if (error != null)
        {
            var title = statusCode == 409 ? "Conflict" : "Not Found";
            var type = statusCode == 409 ? "https://httpstatuses.io/409" : "https://httpstatuses.io/404";
            return Problem("Ошибка обработки");
        }

        return Ok(response);
    }

    [HttpGet("{id}/segments")]
    public IActionResult GetVideoSegments(string id)
    {
        var (response, error, statusCode) = _applicationService.GetVideoSegments(id);
        if (error != null)
        {
            return Problem("Ошибка обработки");
        }

        return Ok(response);
    }
}
