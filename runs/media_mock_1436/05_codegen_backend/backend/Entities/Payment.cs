namespace Generated.Api.Entities;

public class Payment
{
    public Guid Id { get; set; } = string.Empty;
    public string Sessionid { get; set; } = string.Empty;
    public decimal Amount { get; set; }
    public string Status { get; set; } = string.Empty;
}
