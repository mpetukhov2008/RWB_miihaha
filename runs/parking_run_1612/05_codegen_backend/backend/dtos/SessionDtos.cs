namespace ParkingApi.Dtos;

public record StartSessionRequest(string ZoneId, double? Latitude, double? Longitude);
public record SessionDto(string Id, string ZoneId, string ZoneName, DateTime StartedAt, decimal RatePerHour, string Currency, string Status, DateTime? EndedAt = null, int? DurationSeconds = null, decimal? Amount = null, decimal? CurrentAmount = null);
public record PaymentDto(string Id, decimal Amount, string Status, DateTime? PaidAt = null);
public record StartSessionResponse(SessionDto Session, PaymentDto Payment);
public record EndSessionResponse(SessionDto Session, PaymentDto Payment);
public record ActiveSessionResponse(SessionDto? Session);
public record ListSessionsRequest(int Limit = 20, int Offset = 0);
public record SessionListItemDto(string Id, string ZoneId, string ZoneName, DateTime StartedAt, DateTime? EndedAt, int? DurationSeconds, decimal? Amount, string Currency, string Status);
public record SessionsResponse(List<SessionListItemDto> Items, int Total);
public record AdminListSessionsRequest(string? ZoneId, string? Status, int Limit = 50, int Offset = 0);
public record AdminSessionListItemDto(string Id, string UserId, string ZoneId, string ZoneName, DateTime StartedAt, DateTime? EndedAt, int? DurationSeconds, decimal? Amount, string Currency, string Status);
public record AdminSessionsResponse(List<AdminSessionListItemDto> Items, int Total);