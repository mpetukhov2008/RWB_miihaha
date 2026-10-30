using NetTopologySuite.Geometries;

namespace Generated.Api.Geo;

/// <summary>
/// Сервис гео-поиска: определяет ближайшую зону по координатам.
/// </summary>
public class GeoService
{
    /// <summary>Найти зону, содержащую точку, или ближайшую к ней.</summary>
    public ParkingZone? FindZone(IEnumerable<ParkingZone> zones, double lat, double lng)
    {
        var point = new Point(lng, lat) { SRID = 4326 };

        ParkingZone? best = null;
        double bestDistance = double.MaxValue;

        foreach (var zone in zones)
        {
            if (zone.Geometry.Contains(point))
            {
                return zone;
            }

            var distance = zone.Geometry.Distance(point);
            if (distance < bestDistance)
            {
                bestDistance = distance;
                best = zone;
            }
        }

        return best;
    }
}
