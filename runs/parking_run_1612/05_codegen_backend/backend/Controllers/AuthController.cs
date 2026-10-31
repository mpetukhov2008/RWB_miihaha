using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("auth")]
public class AuthController : ControllerBase
{
    private readonly AuthService _auth;
    public AuthController(AuthService auth) => _auth = auth;

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest req)
    {
        var (ok, err) = _auth.Login(req);
        if (ok is null) return Problem(statusCode: 401, title: "Unauthorized", detail: err);
        return Ok(ok);
    }
}