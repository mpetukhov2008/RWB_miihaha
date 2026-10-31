using ParkingApi.Dtos;
using ParkingApi.Entities;

namespace ParkingApi.Services;

public class NotificationService
{
    private readonly InMemoryStore _store;
    public NotificationService(InMemoryStore store) => _store = store;

    public NotificationsResponse List(string userId, bool unreadOnly, int limit)
    {
        var q = _store.Notifications.Where(n => n.UserId == userId);
        if (unreadOnly) q = q.Where(n => n.ReadAt is null);
        var items = q.OrderByDescending(n => n.SentAt).Take(limit).Select(n => new NotificationDto(n.Id, n.Type, n.Message, n.SentAt, n.ReadAt)).ToList();
        return new NotificationsResponse(items);
    }

    public (MarkReadResponse? Ok, bool NotFound) MarkRead(string notificationId, string userId)
    {
        var n = _store.Notifications.FirstOrDefault(x => x.Id == notificationId && x.UserId == userId);
        if (n is null) return (null, true);
        n.ReadAt = DateTime.UtcNow;
        return (new MarkReadResponse(n.Id, n.ReadAt.Value), false);
    }
}