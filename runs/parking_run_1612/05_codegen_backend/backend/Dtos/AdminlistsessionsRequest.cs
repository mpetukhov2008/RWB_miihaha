namespace Generated.Api.Dtos;

public record AdminlistsessionsRequest
(
    ZoneId string,
    Status string,
    Limit decimal,
    Offset decimal
);
