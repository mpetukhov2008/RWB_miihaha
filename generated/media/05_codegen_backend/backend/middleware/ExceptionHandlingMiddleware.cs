using System.Net;
using System.Text.Json;
using MediaProcessingApi.Exceptions;

namespace MediaProcessingApi.Middleware;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;

    public ExceptionHandlingMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        var (statusCode, title, detail) = exception switch
        {
            BadRequestException ex => (HttpStatusCode.BadRequest, "Bad Request", ex.Message),
            NotFoundException ex => (HttpStatusCode.NotFound, "Not Found", ex.Message),
            ConflictException ex => (HttpStatusCode.Conflict, "Conflict", ex.Message),
            _ => (HttpStatusCode.InternalServerError, "Internal Server Error", "An unexpected error occurred.")
        };

        context.Response.StatusCode = (int)statusCode;
        context.Response.ContentType = "application/problem+json";

        var problemDetails = new
        {
            type = $"https://httpstatuses.com/{(int)statusCode}",
            title = title,
            status = (int)statusCode,
            detail = detail,
            instance = context.Request.Path
        };

        var json = JsonSerializer.Serialize(problemDetails);
        await context.Response.WriteAsync(json);
    }
}
