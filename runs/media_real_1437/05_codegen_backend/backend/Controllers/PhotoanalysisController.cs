using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/PhotoAnalysis")]
public class PhotoanalysisController(AppDbContext db) : ControllerBase
{

    /// <summary>Получить результат анализа фотографии.</summary>
    [Authorize]
    [HttpGet("applications/{id}/photo-result")]
    public IActionResult Getphotoanalysisresult()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "getPhotoAnalysisResult" });
    }
}
