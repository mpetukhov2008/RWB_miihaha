using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/sessions")]
public class SessionsController(AppDbContext db) : ControllerBase
{

    /// <summary>Начать сессию</summary>
    [Authorize]
    [HttpPost]
    public IActionResult Startsession()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "startSession" });
    }

    /// <summary>Завершить сессию</summary>
    [Authorize]
    [HttpPost("{sessionId}/complete")]
    public IActionResult Completesession()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "completeSession" });
    }

    /// <summary>История сессий</summary>
    [Authorize]
    [HttpGet]
    public IActionResult Listsessions()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "listSessions" });
    }
}
