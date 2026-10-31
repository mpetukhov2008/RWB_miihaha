using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/admin")]
public class AdminController(AppDbContext db) : ControllerBase
{

    /// <summary>Создать зону</summary>
    [Authorize]
    [HttpPost("zones")]
    public IActionResult Createzone()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "createZone" });
    }
}
