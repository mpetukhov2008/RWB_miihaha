namespace Generated.Api.Entities;

/// <summary>Mock-платёж сессии (сущность-пример, заменяется генератором).</summary>
public class Payment
{
    public Guid Id { get; set; }
    public Guid SessionId { get; set; }
    public decimal Amount { get; set; }
    public string Status { get; set; } = "pending"; // pending | paid
}
