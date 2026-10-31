using Microsoft.AspNetCore.Mvc;
using MediaProcessingApi.Dtos;
using MediaProcessingApi.Services;

namespace MediaProcessingApi.Controllers;

[ApiController]
[Route("webhooks")]
[Authorize]
public class WebhooksController : ControllerBase
{
    private readonly IWebhookService _webhookService;

    public WebhooksController(IWebhookService webhookService)
    {
        _webhookService = webhookService;
    }

    [HttpPost("status")]
    [ProducesResponseType(typeof(ReceiveStatusWebhookResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> ReceiveStatusWebhook([FromBody] ReceiveStatusWebhookRequest request)
    {
        var response = await _webhookService.ReceiveStatusWebhookAsync(request);
        return Ok(response);
    }
}
