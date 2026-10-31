using ParkingApi.Dtos;
using ParkingApi.Entities;

namespace ParkingApi.Services;

public class SessionService
{
    private readonly InMemoryStore _store;
    public SessionService(InMemoryStore store) => _store = store;

    public (StartSessionResponse? Ok, string? Error, int Code) Start(StartSessionRequest req, string userId)
    {
        if (string.IsNullOrWhiteSpace(req.ZoneId)) return (null, "zone_id обязателен", 422);
        var zone = _store.Zones.FirstOrDefault(z => z.Id == req.ZoneId && z.IsActive);
        if (zone is null) return (null, "Зона не найдена или неактивна", 422);
        if (_store.Sessions.Any(s => s.UserId == userId && s.Status == "active"))
            return (null, "У вас уже есть активная сессия", 409);
        var session = new ParkingSession { UserId = userId, ZoneId = zone.Id, RatePerHour = zone.RatePerHour, Status = "active" };
        _store.Sessions.Add(session);
        var payment = new Payment { SessionId = session.Id, Amount = zone.RatePerHour, Status = "pending" };
        _store.Payments.Add(payment);
        _store.Notifications.Add(new Notification { UserId = userId, SessionId = session.Id, Type = "session_started", Message = $"Сессия в зоне {zone.Name} начата", SentAt = DateTime.UtcNow });
        return (new StartSessionResponse(Map(session, zone.Name), new PaymentDto(payment.Id, payment.Amount, payment.Status)), null, 200);
    }

    public ActiveSessionResponse GetActive(string userId)
    {
        var s = _store.Sessions.FirstOrDefault(x => x.UserId == userId && x.Status == "active");
        if (s is null) return new ActiveSessionResponse(null);
        var zone = _store.Zones.FirstOrDefault(z => z.Id == s.ZoneId);
        var hours = (DateTime.UtcNow - s.StartedAt).TotalHours;
        var current = Math.Round(s.RatePerHour * hours, 2);
        var dto = Map(s, zone?.Name ?? "");
        return new ActiveSessionResponse(new SessionDto(dto.Id, dto.ZoneId, dto.ZoneName, dto.StartedAt, dto.RatePerHour, dto.Currency, dto.Status, dto.EndedAt, dto.DurationSeconds, dto.Amount, current));
    }

    public (EndSessionResponse? Ok, string? Error, int Code) End(string sessionId, string userId)
    {
        var s = _store.Sessions.FirstOrDefault(x => x.Id == sessionId);
        if (s is null || s.UserId != userId) return (null, "Сессия не найдена", 404);
        if (s.Status != "active") return (null, "Сессия уже завершена", 409);
        s.EndedAt = DateTime.UtcNow;
        s.DurationSeconds = (int)(s.EndedAt.Value - s.StartedAt).TotalSeconds;
        s.Amount = Math.Round(s.RatePerHour * s.DurationSeconds.Value / 3600.0, 2);
        s.Status = "completed";
        var payment = _store.Payments.FirstOrDefault(p => p.SessionId == s.Id);
        if (payment is not null) { payment.Amount = s.Amount.Value; payment.Status = "paid"; payment.PaidAt = DateTime.UtcNow; }
        var zone = _store.Zones.FirstOrDefault(z => z.Id == s.ZoneId);
        return (new EndSessionResponse(Map(s, zone?.Name ?? ""), new PaymentDto(payment!.Id, payment.Amount, payment.Status, payment.PaidAt)), null, 200);
    }

    public SessionsResponse ListMy(string userId, int limit, int offset)
    {
        var all = _store.Sessions.Where(s => s.UserId == userId).OrderByDescending(s => s.StartedAt).ToList();
        var items = all.Skip(offset).Take(limit).Select(s => MapItem(s)).ToList();
        return new SessionsResponse(items, all.Count);
    }

    public AdminSessionsResponse AdminList(string? zoneId, string? status, int limit, int offset)
    {
        var q = _store.Sessions.AsEnumerable();
        if (!string.IsNullOrWhiteSpace(zoneId)) q = q.Where(s => s.ZoneId == zoneId);
        if (!string.IsNullOrWhiteSpace(status)) q = q.Where(s => s.Status == status);
        var all = q.OrderByDescending(s => s.StartedAt).ToList();
        var items = all.Skip(offset).Take(limit).Select(s => new AdminSessionListItemDto(s.Id, s.UserId, s.ZoneId, _store.Zones.FirstOrDefault(z => z.Id == s.ZoneId)?.Name ?? "", s.StartedAt, s.EndedAt, s.DurationSeconds, s.Amount, _store.Zones.FirstOrDefault(z => z.Id == s.ZoneId)?.Currency ?? "RUB", s.Status)).ToList();
        return new AdminSessionsResponse(items, all.Count);
    }

    private static SessionDto Map(ParkingSession s, string zoneName) => new(s.Id, s.ZoneId, zoneName, s.StartedAt, s.RatePerHour, _storeCurrency(s), s.Status, s.EndedAt, s.DurationSeconds, s.Amount);
    private static string _storeCurrency(ParkingSession s) => "RUB";
    private static SessionListItemDto MapItem(ParkingSession s) => new(s.Id, s.ZoneId, "", s.StartedAt, s.EndedAt, s.DurationSeconds, s.Amount, "RUB", s.Status);
}