namespace ParkingApi.Dtos;

public record NearbyZoneRequest(double Latitude, double Longitude);
public record ZoneDto(string Id, string Name, decimal RatePerHour, string Currency);
public record NearbyZoneResponse(bool InZone, ZoneDto? Zone);
public record CreateZoneRequest(string Name, string Polygon, decimal RatePerHour, string? Currency = "RUB", bool IsActive = true);
public record UpdateZoneRequest(string? Name, string? Polygon, decimal? RatePerHour, string? Currency, bool? IsActive);
public record ZoneCreatedDto(string Id, string Name, decimal RatePerHour, string Currency, bool IsActive, DateTime CreatedAt);
public record ZoneUpdatedDto(string Id, string Name, decimal RatePerHour, string Currency, bool IsActive, DateTime UpdatedAt);
public record AdminZoneDto(string Id, string Name, decimal RatePerHour, string Currency, bool IsActive, DateTime? UpdatedAt);
public record AdminZonesResponse(List<AdminZoneDto> Items);