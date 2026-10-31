using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ParkingApi.Dtos;
using ParkingApi.Services;

namespace ParkingApi.Controllers;

[ApiController]
[Route("notifications")]
[Authorize]
public class NotificationsController : ControllerBase
{
    private readonly NotificationService _notifications;
    public NotificationsController(NotificationService notifications) => _notifications = notifications;

    private string UserId => User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value ?? "";

    [HttpGet]
    public IActionResult List([FromBody] ListNotificationsRequest? req)
    {
        return Ok(_notifications.List(UserId, req?.UnreadOnly ?? false, req?.Limit ?? 20));
    }

    [HttpPost("{notificationId}/read")]
    public IActionResult MarkRead(string notificationId)
    {
        var (ok, notFound) = _notifications.MarkRead(notificationId, UserId);
        if (notFound) return Problem(statusCode: 404, title: "Not Found", detail: "Уведомление не найдено");
        return Ok(ok);
    }
}