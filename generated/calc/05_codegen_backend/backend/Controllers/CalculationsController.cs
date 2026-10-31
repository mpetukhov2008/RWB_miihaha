using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Api.Controllers;

[ApiController]
[Route("calculations")]
public class CalculationsController : ControllerBase
{
    private readonly CalculationService _calculationService;

    public CalculationsController(CalculationService calculationService)
    {
        _calculationService = calculationService;
    }

    [HttpPost]
    [ProducesResponseType(typeof(CalculationResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> CreateCalculation([FromBody] CreateCalculationRequest request)
    {
        if (request is null || request.FirstNumber is null || request.SecondNumber is null)
        {
            return BadRequest(new ProblemDetails
            {
                Type = "https://tools.ietf.org/html/rfc9457",
                Title = "Bad Request",
                Status = StatusCodes.Status400BadRequest,
                Detail = "Поля first_number и second_number обязательны.",
                Instance = "/calculations"
            });
        }

        try
        {
            var result = await _calculationService.CreateCalculationAsync(request.FirstNumber.Value, request.SecondNumber.Value);
            return Ok(result);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new ProblemDetails
            {
                Type = "https://tools.ietf.org/html/rfc9457",
                Title = "Bad Request",
                Status = StatusCodes.Status400BadRequest,
                Detail = ex.Message,
                Instance = "/calculations"
            });
        }
        catch (Exception ex)
        {
            return StatusCode(StatusCodes.Status500InternalServerError, new ProblemDetails
            {
                Type = "https://tools.ietf.org/html/rfc9457",
                Title = "Internal Server Error",
                Status = StatusCodes.Status500InternalServerError,
                Detail = ex.Message,
                Instance = "/calculations"
            });
        }
    }
}
