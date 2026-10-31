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
    private readonly PhotoAnalysisService _photoAnalysisService;
    private readonly VideoAnalysisService _videoAnalysisService;

    public ApplicationsController(
        ApplicationService applicationService,
        PhotoAnalysisService photoAnalysisService,
        VideoAnalysisService videoAnalysisService)
    {
        _applicationService = applicationService;
        _photoAnalysisService = photoAnalysisService;
        _videoAnalysisService = videoAnalysisService;
    }

    [HttpPost]
    public IActionResult CreateApplication([FromBody] CreateApplicationRequest request)
    {
        var (response, error, statusCode) = _applicationService.CreateApplication(request);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 400,
                title: "Error");
        }

        return Created($"/applications/{response!.Id}", response);
    }

    [HttpGet("{id}")]
    public IActionResult GetApplication(string id)
    {
        var (response, error, statusCode) = _applicationService.GetApplication(id);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 404,
                title: "Error");
        }

        return Ok(response);
    }

    [HttpGet("{id}/photo-result")]
    public IActionResult GetPhotoAnalysisResult(string id)
    {
        var (response, error, statusCode) = _photoAnalysisService.GetPhotoAnalysisResult(id);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 404,
                title: "Error");
        }

        return Ok(response);
    }

    [HttpGet("{id}/video-result")]
    public IActionResult GetVideoAnalysisResult(string id)
    {
        var (response, error, statusCode) = _videoAnalysisService.GetVideoAnalysisResult(id);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 404,
                title: "Error");
        }

        return Ok(response);
    }

    [HttpPost("{id}/process")]
    public IActionResult TriggerProcessing(string id)
    {
        var (response, error, statusCode) = _applicationService.TriggerProcessing(id);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 409,
                title: "Error");
        }

        return Ok(response);
    }
}
