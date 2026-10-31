namespace ParkingApi.Dtos;

public record ListNotificationsRequest(bool UnreadOnly = false, int Limit = 20);
public record NotificationDto(string Id, string Type, string Message, DateTime SentAt, DateTime? ReadAt);
public record NotificationsResponse(List<NotificationDto> Items);
public record MarkReadResponse(string Id, DateTime ReadAt);