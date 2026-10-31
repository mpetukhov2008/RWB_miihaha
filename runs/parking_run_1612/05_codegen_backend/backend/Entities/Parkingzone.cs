namespace ParkingApi.Entities;

public class ParkingZone
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Name { get; set; } = string.Empty;
    public string Polygon { get; set; } = string.Empty;
    public decimal RatePerHour { get; set; }
    public string Currency { get; set; } = "RUB";
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
}