using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/VideoAnalysis")]
public class VideoanalysisController(AppDbContext db) : ControllerBase
{

    /// <summary>Получить результат анализа видеопотока с временными метками.</summary>
    [Authorize]
    [HttpGet("applications/{id}/video-result")]
    public IActionResult Getvideoanalysisresult()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "getVideoAnalysisResult" });
    }
}
