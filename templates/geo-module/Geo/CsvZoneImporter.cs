using System.Globalization;
using NetTopologySuite.IO;

namespace Generated.Api.Geo;

/// <summary>Импорт зон из CSV (пример: name;tariff;wkt).</summary>
public static class CsvZoneImporter
{
    public static List<ParkingZone> Parse(string csv)
    {
        var zones = new List<ParkingZone>();
        foreach (var line in csv.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var parts = line.Split(';');
            if (parts.Length < 3)
            {
                continue;
            }

            zones.Add(new ParkingZone
            {
                Id = Guid.NewGuid(),
                Name = parts[0].Trim(),
                TariffPerHour = decimal.Parse(parts[1].Trim(), CultureInfo.InvariantCulture),
                Geometry = WKTReader.Parse(parts[2].Trim()),
            });
        }
        return zones;
    }
}
