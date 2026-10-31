namespace Generated.Api.Dtos;

public record AdminupdatezoneRequest
(
    Name string,
    Polygon string,
    RatePerHour decimal,
    Currency string,
    IsActive bool
);
