namespace ParkingApi.Dtos;

public record LoginRequest(string Email, string Password);
public record AuthUserDto(string Id, string Email, string Role);
public record LoginResponse(string Token, AuthUserDto User);