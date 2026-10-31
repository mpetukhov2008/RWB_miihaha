using System.Text.Json.Serialization;

namespace Api.Dtos;

public class CreateCalculationRequest
{
    [JsonPropertyName("first_number")]
    public decimal? FirstNumber { get; set; }

    [JsonPropertyName("second_number")]
    public decimal? SecondNumber { get; set; }
}
