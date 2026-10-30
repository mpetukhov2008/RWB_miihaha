using Microsoft.AspNetCore.Mvc;

namespace Generated.Api.Common;

/// <summary>
/// Единый формат ошибок API — ProblemDetails (RFC 7807).
/// Любой контроллер возвращает ошибки через Problem(...), а не сырые JSON.
/// </summary>
public static class ProblemDetailsExtensions
{
    /// <summary>Создать ProblemDetails с кодом и деталями.</summary>
    public static ProblemDetails Problem(
        this ControllerBase controller,
        int status,
        string title,
        string detail,
        string? instance = null)
    {
        return new ProblemDetails
        {
            Type = $"https://api.local/problems/{status}",
            Title = title,
            Status = status,
            Detail = detail,
            Instance = instance,
        };
    }
}
