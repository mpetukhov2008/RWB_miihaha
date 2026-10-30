using System.Collections.Generic;

namespace Generated.Api.Mocks;

/// <summary>Интерфейс источника парковочных зон.</summary>
public interface IParkingProvider
{
    IReadOnlyList<global::Generated.Api.Entities.ParkingZone> LoadZones();
}

/// <summary>Mock-источник зон для тестов и демо.</summary>
public class InMemoryParkingProvider(IReadOnlyList<global::Generated.Api.Entities.ParkingZone> zones)
    : IParkingProvider
{
    public IReadOnlyList<global::Generated.Api.Entities.ParkingZone> LoadZones() => zones;
}
