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
            return Problem(
                detail: error,
                statusCode: statusCode ?? 400,
                title: "Error");
        }

        return Ok(response);
    }

    [HttpPost("{id}/confirm-upload")]
    public IActionResult ConfirmFileUpload(string id)
    {
        var (response, error, statusCode) = _fileService.ConfirmFileUpload(id);
        if (error != null)
        {
            return Problem(
                detail: error,
                statusCode: statusCode ?? 404,
                title: "Error");
        }

        return Ok(response);
    }
}
