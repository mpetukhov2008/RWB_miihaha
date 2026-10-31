using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("zones")]
[Authorize]
public class ZonesController : ControllerBase
{
    private readonly ZoneService _zones;
    public ZonesController(ZoneService zones) => _zones = zones;

    [HttpGet("nearby")]
    public IActionResult GetNearby([FromBody] NearbyZoneRequest req)
    {
        return Ok(_zones.GetNearby(req));
    }
}