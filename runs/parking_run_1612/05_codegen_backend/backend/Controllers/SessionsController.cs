using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("sessions")]
[Authorize]
public class SessionsController : ControllerBase
{
    private readonly SessionService _sessions;
    public SessionsController(SessionService sessions) => _sessions = sessions;

    private string UserId => User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value ?? "";

    [HttpPost]
    public IActionResult Start([FromBody] StartSessionRequest req)
    {
        var (ok, err, code) = _sessions.Start(req, UserId);
        if (ok is null) return Problem(statusCode: code, title: code == 409 ? "Conflict" : "Unprocessable Entity", detail: err);
        return CreatedAtAction(nameof(Start), null, ok);
    }

    [HttpGet("active")]
    public IActionResult GetActive()
    {
        return Ok(_sessions.GetActive(UserId));
    }

    [HttpGet]
    public IActionResult ListMy([FromBody] ListSessionsRequest? req)
    {
        return Ok(_sessions.ListMy(UserId, req?.Limit ?? 20, req?.Offset ?? 0));
    }

    [HttpPost("{sessionId}/end")]
    public IActionResult End(string sessionId)
    {
        var (ok, err, code) = _sessions.End(sessionId, UserId);
        if (ok is null) return Problem(statusCode: code, title: code == 404 ? "Not Found" : "Conflict", detail: err);
        return Ok(ok);
    }
}