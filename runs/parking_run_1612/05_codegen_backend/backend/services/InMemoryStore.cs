using ParkingApi.Entities;

namespace ParkingApi.Services;

public class InMemoryStore
{
    public List<User> Users { get; } = new();
    public List<ParkingZone> Zones { get; } = new();
    public List<ParkingSession> Sessions { get; } = new();
    public List<Payment> Payments { get; } = new();
    public List<Notification> Notifications { get; } = new();

    public InMemoryStore()
    {
        Users.Add(new User { Id = "u-admin", Email = "admin@test.ru", Role = "admin", Password = "admin123" });
        Users.Add(new User { Id = "u-driver", Email = "driver@test.ru", Role = "driver", Password = "driver123" });
        Zones.Add(new ParkingZone { Id = "z-1", Name = "Центр", Polygon = "POLYGON((0 0,1 0,1 1,0 1,0 0))", RatePerHour = 100m, Currency = "RUB", IsActive = true });
    }
}