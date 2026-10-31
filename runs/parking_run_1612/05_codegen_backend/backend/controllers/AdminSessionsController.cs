using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("admin/sessions")]
[Authorize(Roles = "admin")]
public class AdminSessionsController : ControllerBase
{
    private readonly SessionService _sessions;
    public AdminSessionsController(SessionService sessions) => _sessions = sessions;

    [HttpGet]
    public IActionResult List([FromBody] AdminListSessionsRequest? req)
    {
        return Ok(_sessions.AdminList(req?.ZoneId, req?.Status, req?.Limit ?? 50, req?.Offset ?? 0));
    }
}