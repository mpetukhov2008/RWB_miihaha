using ParkingApi.Dtos;
using ParkingApi.Entities;

namespace ParkingApi.Services;

public class AuthService
{
    private readonly InMemoryStore _store;
    public AuthService(InMemoryStore store) => _store = store;

    public (LoginResponse? Ok, string? Error) Login(LoginRequest req)
    {
        var user = _store.Users.FirstOrDefault(u => u.Email == req.Email);
        if (user is null || user.Password != req.Password)
            return (null, "Неверный email или пароль");
        var token = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes($"{user.Id}:{user.Role}"));
        return (new LoginResponse(token, new AuthUserDto(user.Id, user.Email, user.Role)), null);
    }
}