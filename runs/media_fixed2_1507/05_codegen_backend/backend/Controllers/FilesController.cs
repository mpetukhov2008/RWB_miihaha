using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MediaProcessingApi.Dtos;
using MediaProcessingApi.Services;

namespace MediaProcessingApi.Controllers;

[ApiController]
[Route("files")]
[Authorize]
public class FilesController : ControllerBase
{
    private readonly FileService _fileService;

    public FilesController(FileService fileService)
    {
        _fileService = fileService;
    }

    [HttpPost("upload-url")]
    public IActionResult GetUploadUrl([FromBody] GetUploadUrlRequest request)
    {
        var (response, error, statusCode) = _fileService.GetUploadUrl(request);
        if (error != null)
        {
            return Problem(new ProblemDetails
            {
                Type = "https://httpstatuses.io/400",
                Title = "Bad Request",
                Status = statusCode ?? 400,
                Detail = error
            });
        }

        return Ok(response);
    }

    [HttpPost("{id}/confirm")]
    public IActionResult ConfirmFileUpload(string id)
    {
        var (response, error, statusCode) = _fileService.ConfirmFileUpload(id);
        if (error != null)
        {
            return Problem(new ProblemDetails
            {
                Type = "https://httpstatuses.io/404",
                Title = "Not Found",
                Status = statusCode ?? 404,
                Detail = error
            });
        }

        return Ok(response);
    }

    [HttpGet("{id}/download-url")]
    public IActionResult GetDownloadUrl(string id)
    {
        var (response, error, statusCode) = _fileService.GetDownloadUrl(id);
        if (error != null)
        {
            return Problem(new ProblemDetails
            {
                Type = "https://httpstatuses.io/404",
                Title = "Not Found",
                Status = statusCode ?? 404,
                Detail = error
            });
        }

        return Ok(response);
    }
}
