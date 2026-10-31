namespace Generated.Api.Entities;

public class Session
{
    public Guid Id { get; set; } = string.Empty;
    public string Userid { get; set; } = string.Empty;
    public string Zoneid { get; set; } = string.Empty;
    public object Startedat { get; set; }
    public object Endedat { get; set; }
    public string Status { get; set; } = string.Empty;
}
