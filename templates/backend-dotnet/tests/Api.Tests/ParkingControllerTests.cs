using Generated.Api.Controllers;
using Generated.Api.Data;
using Generated.Api.Entities;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NetTopologySuite.Geometries;

namespace Generated.Api.Tests;

public sealed class ParkingControllerTests : IDisposable
{
    private readonly AppDbContext _db;
    private readonly ParkingController _controller;
    private readonly Guid _zoneId;

    public ParkingControllerTests()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        _db = new AppDbContext(options);

        var zone = new ParkingZone
        {
            Id = Guid.NewGuid(),
            Name = "Test Zone",
            TariffPerHour = 200m,
            Geometry = GeometryFactory.Default.CreateLineString(
            [
                new Coordinate(30.3, 59.9),
                new Coordinate(30.31, 59.91),
            ]),
        };
        _db.ParkingZones.Add(zone);
        _db.SaveChanges();
        _zoneId = zone.Id;

        _controller = new ParkingController(_db)
        {
            ControllerContext = new ControllerContext
            {
                HttpContext = new DefaultHttpContext(),
            },
        };
    }

    [Fact]
    public async Task GetZone_Returns200_WhenZoneExists()
    {
        var result = await _controller.GetZone(_zoneId, CancellationToken.None);

        var ok = Assert.IsType<OkObjectResult>(result);
        var zone = Assert.IsType<ParkingZone>(ok.Value);
        Assert.Equal("Test Zone", zone.Name);
    }

    [Fact]
    public async Task GetZone_Returns404ProblemDetails_WhenZoneMissing()
    {
        var result = await _controller.GetZone(Guid.NewGuid(), CancellationToken.None);

        var notFound = Assert.IsType<NotFoundObjectResult>(result);
        var problem = Assert.IsType<ProblemDetails>(notFound.Value);
        Assert.Equal(StatusCodes.Status404NotFound, problem.Status);
    }

    [Fact]
    public async Task StartSession_Returns400_WhenIdempotencyKeyMissing()
    {
        var request = new StartSessionRequest(_zoneId);

        var result = await _controller.StartSession(request, idempotencyKey: null, CancellationToken.None);

        var badRequest = Assert.IsType<BadRequestObjectResult>(result);
        var problem = Assert.IsType<ProblemDetails>(badRequest.Value);
        Assert.Equal(StatusCodes.Status400BadRequest, problem.Status);
    }

    [Fact]
    public async Task StartSession_IsIdempotent_ForSameKey()
    {
        var request = new StartSessionRequest(_zoneId);

        var first = await _controller.StartSession(request, "key-1", CancellationToken.None);
        var second = await _controller.StartSession(request, "key-1", CancellationToken.None);

        var created = Assert.IsType<ObjectResult>(first);
        var firstSession = Assert.IsType<Session>(created.Value);
        var ok = Assert.IsType<OkObjectResult>(second);
        var secondSession = Assert.IsType<Session>(ok.Value);
        Assert.Equal(firstSession.Id, secondSession.Id);
        Assert.Single(_db.Sessions);
    }

    [Fact]
    public async Task CompleteSession_MarksPaymentPaid_AndSessionCompleted()
    {
        var session = new Session
        {
            Id = Guid.NewGuid(),
            UserId = Guid.NewGuid(),
            ZoneId = _zoneId,
            StartedAt = DateTimeOffset.UtcNow,
            Status = "active",
            IdempotencyKey = "key-2",
        };
        _db.Sessions.Add(session);
        _db.Payments.Add(new Payment
        {
            Id = Guid.NewGuid(),
            SessionId = session.Id,
            Amount = 0m,
            Status = "pending",
        });
        await _db.SaveChangesAsync();

        var result = await _controller.CompleteSession(session.Id, CancellationToken.None);

        var ok = Assert.IsType<OkObjectResult>(result);
        var completed = Assert.IsType<Session>(ok.Value);
        Assert.Equal("completed", completed.Status);
        Assert.NotNull(completed.EndedAt);

        var payment = await _db.Payments.SingleAsync(p => p.SessionId == session.Id);
        Assert.Equal("paid", payment.Status);
        Assert.True(payment.Amount >= 0m);
    }

    public void Dispose() => _db.Dispose();
}
