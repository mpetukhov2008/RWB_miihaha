using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/zones")]
public class ZonesController(AppDbContext db) : ControllerBase
{

    /// <summary>Получить зону</summary>
    [HttpGet("{zoneId}")]
    public IActionResult Getzone()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "getZone" });
    }

    /// <summary>Создать зону</summary>
    [Authorize]
    [HttpPost("admin")]
    public IActionResult Createzone()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "createZone" });
    }
}
