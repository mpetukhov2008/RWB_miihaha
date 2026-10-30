namespace Generated.Api.Entities;

/// <summary>Парковочная сессия (сущность-пример, заменяется генератором).</summary>
public class Session
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public Guid ZoneId { get; set; }
    public DateTimeOffset StartedAt { get; set; }
    public DateTimeOffset? EndedAt { get; set; }
    public string Status { get; set; } = "active"; // active | completed
}
