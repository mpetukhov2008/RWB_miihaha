using NetTopologySuite.Geometries;

namespace Generated.Api.Entities;

/// <summary>Платная парковочная зона (сущность-пример, заменяется генератором).</summary>
public class ParkingZone
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal TariffPerHour { get; set; }
    public Geometry Geometry { get; set; } = null!;
}
