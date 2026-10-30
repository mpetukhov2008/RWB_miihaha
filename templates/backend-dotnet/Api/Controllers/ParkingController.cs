using Generated.Api.Common;
using Generated.Api.Data;
using Generated.Api.Entities;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Generated.Api.Controllers;

/// <summary>
/// Контроллер-пример. Генератор заменяет его контроллерами из операций OpenAPI.
/// </summary>
[ApiController]
[Route("api")]
public class ParkingController(AppDbContext db) : ControllerBase
{
    /// <summary>Получить зону по ID.</summary>
    [HttpGet("zones/{zoneId:guid}")]
    [ProducesResponseType(typeof(ParkingZone), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetZone(Guid zoneId, CancellationToken ct)
    {
        var zone = await db.ParkingZones.FindAsync([zoneId], ct);
        if (zone is null)
        {
            return NotFound(this.Problem(404, "Not Found", $"Zone {zoneId} not found"));
        }
        return Ok(zone);
    }

    /// <summary>Начать сессию (идемпотентность по Idempotency-Key).</summary>
    [HttpPost("sessions")]
    [Authorize]
    [ProducesResponseType(typeof(Session), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> StartSession(
        [FromBody] StartSessionRequest request,
        [FromHeader(Name = "Idempotency-Key")] string? idempotencyKey,
        CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(idempotencyKey))
        {
            return BadRequest(this.Problem(400, "Bad Request", "Idempotency-Key header is required"));
        }

        var zone = await db.ParkingZones.FindAsync([request.ZoneId], ct);
        if (zone is null)
        {
            return NotFound(this.Problem(404, "Not Found", $"Zone {request.ZoneId} not found"));
        }

        // Идемпотентность: если ключ уже использован — вернуть существующую сессию.
        var existing = await db.Sessions
            .FirstOrDefaultAsync(s => s.IdempotencyKey == idempotencyKey, ct);
        if (existing is not null)
        {
            return Ok(existing);
        }

        var session = new Session
        {
            Id = Guid.NewGuid(),
            UserId = Guid.NewGuid(), // в реальном коде — из Claims
            ZoneId = zone.Id,
            StartedAt = DateTimeOffset.UtcNow,
            Status = "active",
            IdempotencyKey = idempotencyKey,
        };
        db.Sessions.Add(session);

        db.Payments.Add(new Payment
        {
            Id = Guid.NewGuid(),
            SessionId = session.Id,
            Amount = zone.TariffPerHour,
            Status = "pending",
        });

        await db.SaveChangesAsync(ct);
        return StatusCode(StatusCodes.Status201Created, session);
    }

    /// <summary>Завершить сессию.</summary>
    [HttpPost("sessions/{sessionId:guid}/complete")]
    [Authorize]
    [ProducesResponseType(typeof(Session), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> CompleteSession(Guid sessionId, CancellationToken ct)
    {
        var session = await db.Sessions.FindAsync([sessionId], ct);
        if (session is null)
        {
            return NotFound(this.Problem(404, "Not Found", $"Session {sessionId} not found"));
        }

        session.EndedAt = DateTimeOffset.UtcNow;
        session.Status = "completed";

        var payment = await db.Payments.FirstOrDefaultAsync(p => p.SessionId == sessionId, ct);
        if (payment is not null)
        {
            var zone = await db.ParkingZones.FindAsync([session.ZoneId], ct);
            var hours = (decimal)(session.EndedAt - session.StartedAt).Value.TotalHours;
            payment.Amount = zone is null ? 0 : hours * zone.TariffPerHour;
            payment.Status = "paid";
        }

        await db.SaveChangesAsync(ct);
        return Ok(session);
    }

    /// <summary>Создать зону (админ).</summary>
    [HttpPost("admin/zones")]
    [Authorize(Roles = "Administrator")]
    [ProducesResponseType(typeof(ParkingZone), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status403Forbidden)]
    public async Task<IActionResult> CreateZone([FromBody] CreateZoneRequest request, CancellationToken ct)
    {
        var zone = new ParkingZone
        {
            Id = Guid.NewGuid(),
            Name = request.Name,
            TariffPerHour = request.TariffPerHour,
            Geometry = NetTopologySuite.IO.WKTReader.Parse(request.GeometryWkt),
        };
        db.ParkingZones.Add(zone);
        await db.SaveChangesAsync(ct);
        return StatusCode(StatusCodes.Status201Created, zone);
    }
}

/// <summary>Запрос на старт сессии.</summary>
public record StartSessionRequest(Guid ZoneId);

/// <summary>Запрос на создание зоны.</summary>
public record CreateZoneRequest(string Name, decimal TariffPerHour, string GeometryWkt);
