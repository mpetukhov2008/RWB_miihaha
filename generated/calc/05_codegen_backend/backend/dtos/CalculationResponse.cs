using System.Text.Json.Serialization;

namespace Api.Dtos;

public class CalculationResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = string.Empty;

    [JsonPropertyName("first_number")]
    public decimal FirstNumber { get; set; }

    [JsonPropertyName("second_number")]
    public decimal SecondNumber { get; set; }

    [JsonPropertyName("result")]
    public decimal Result { get; set; }

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }
}
