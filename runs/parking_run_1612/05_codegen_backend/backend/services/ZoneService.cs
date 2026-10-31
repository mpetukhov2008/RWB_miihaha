using ParkingApi.Dtos;
using ParkingApi.Entities;

namespace ParkingApi.Services;

public class ZoneService
{
    private readonly InMemoryStore _store;
    public ZoneService(InMemoryStore store) => _store = store;

    public NearbyZoneResponse GetNearby(NearbyZoneRequest req)
    {
        var zone = _store.Zones.FirstOrDefault(z => z.IsActive && Contains(z.Polygon, req.Latitude, req.Longitude));
        return new NearbyZoneResponse(zone is not null, zone is null ? null : new ZoneDto(zone.Id, zone.Name, zone.RatePerHour, zone.Currency));
    }

    public AdminZonesResponse ListZones() => new(_store.Zones.Select(z => new AdminZoneDto(z.Id, z.Name, z.RatePerHour, z.Currency, z.IsActive, z.UpdatedAt)).ToList());

    public (ZoneCreatedDto? Ok, string? Error) Create(CreateZoneRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Name) || string.IsNullOrWhiteSpace(req.Polygon) || req.RatePerHour < 0)
            return (null, "Некорректные данные зоны");
        var zone = new ParkingZone { Name = req.Name, Polygon = req.Polygon, RatePerHour = req.RatePerHour, Currency = req.Currency ?? "RUB", IsActive = req.IsActive };
        _store.Zones.Add(zone);
        return (new ZoneCreatedDto(zone.Id, zone.Name, zone.RatePerHour, zone.Currency, zone.IsActive, zone.CreatedAt), null);
    }

    public (ZoneUpdatedDto? Ok, string? Error, bool NotFound) Update(string zoneId, UpdateZoneRequest req)
    {
        var zone = _store.Zones.FirstOrDefault(z => z.Id == zoneId);
        if (zone is null) return (null, null, true);
        if (req.Name is not null) zone.Name = req.Name;
        if (req.Polygon is not null) zone.Polygon = req.Polygon;
        if (req.RatePerHour is not null) zone.RatePerHour = req.RatePerHour.Value;
        if (req.Currency is not null) zone.Currency = req.Currency;
        if (req.IsActive is not null) zone.IsActive = req.IsActive.Value;
        zone.UpdatedAt = DateTime.UtcNow;
        return (new ZoneUpdatedDto(zone.Id, zone.Name, zone.RatePerHour, zone.Currency, zone.IsActive, zone.UpdatedAt.Value), null, false);
    }

    private static bool Contains(string polygon, double lat, double lon)
    {
        if (!polygon.StartsWith("POLYGON", StringComparison.OrdinalIgnoreCase)) return false;
        var inner = polygon[polygon.IndexOf('(') + 1..];
        inner = inner[..inner.LastIndexOf(')')];
        var pts = inner.Split(',', StringSplitOptions.RemoveEmptyEntries).Select(p => p.Trim().TrimStart('(').TrimEnd(')').Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(double.Parse).ToArray()).Where(p => p.Length == 2).ToArray();
        if (pts.Length < 3) return false;
        bool inside = false;
        for (int i = 0, j = pts.Length - 1; i < pts.Length; j = i++)
        {
            double xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
            if (((yi > lat) != (yj > lat)) && (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi)) inside = !inside;
        }
        return inside;
    }
}