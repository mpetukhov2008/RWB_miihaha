namespace Api.Entities;

public class Calculation
{
    public string Id { get; set; } = string.Empty;
    public decimal FirstNumber { get; set; }
    public decimal SecondNumber { get; set; }
    public decimal Result { get; set; }
    public DateTime CreatedAt { get; set; }
}
