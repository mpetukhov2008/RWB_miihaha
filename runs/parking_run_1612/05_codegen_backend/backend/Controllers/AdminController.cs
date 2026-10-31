using Generated.Api.Common;
using Generated.Api.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
namespace Generated.Api.Controllers;

[ApiController]
[Route("api/admin")]
public class AdminController(AppDbContext db) : ControllerBase
{

    /// <summary>Список всех парковочных зон (админ).</summary>
    [Authorize]
    [HttpGet("zones")]
    public IActionResult Adminlistzones()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "adminListZones" });
    }

    /// <summary>Создание новой парковочной зоны (админ).</summary>
    [Authorize]
    [HttpPost("zones")]
    public IActionResult Admincreatezone()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "adminCreateZone" });
    }

    /// <summary>Редактирование зоны и тарифа (админ).</summary>
    [Authorize]
    [HttpPut("zones/{zone_id}")]
    public IActionResult Adminupdatezone()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "adminUpdateZone" });
    }

    /// <summary>Список активных сессий и истории по зоне (админ).</summary>
    [Authorize]
    [HttpGet("sessions")]
    public IActionResult Adminlistsessions()
    {
        // TODO: бизнес-логика (агент 05/сервисы).
        return Ok(new { Operation = "adminListSessions" });
    }
}
