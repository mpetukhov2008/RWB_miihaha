namespace Generated.Api.Dtos;

public record AdmincreatezoneRequest
(
    Name string,
    Polygon string,
    RatePerHour decimal,
    Currency string,
    IsActive bool
);
