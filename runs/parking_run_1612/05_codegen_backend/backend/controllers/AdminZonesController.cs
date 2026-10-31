using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("admin/zones")]
[Authorize(Roles = "admin")]
public class AdminZonesController : ControllerBase
{
    private readonly ZoneService _zones;
    public AdminZonesController(ZoneService zones) => _zones = zones;

    [HttpGet]
    public IActionResult List() => Ok(_zones.ListZones());

    [HttpPost]
    public IActionResult Create([FromBody] CreateZoneRequest req)
    {
        var (ok, err) = _zones.Create(req);
        if (ok is null) return Problem(statusCode: 422, title: "Unprocessable Entity", detail: err);
        return CreatedAtAction(nameof(List), null, ok);
    }

    [HttpPut("{zoneId}")]
    public IActionResult Update(string zoneId, [FromBody] UpdateZoneRequest req)
    {
        var (ok, err, notFound) = _zones.Update(zoneId, req);
        if (notFound) return Problem(statusCode: 404, title: "Not Found", detail: "Зона не найдена");
        if (ok is null) return Problem(statusCode: 422, title: "Unprocessable Entity", detail: err);
        return Ok(ok);
    }
}