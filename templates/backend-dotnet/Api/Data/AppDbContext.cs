using Generated.Api.Entities;
using Microsoft.EntityFrameworkCore;

namespace Generated.Api.Data;

/// <summary>
/// Контекст БД. Сущности и конфигурация добавляются генератором
/// (см. templates/backend-dotnet/Entities/*.cs).
/// </summary>
public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<ParkingZone> ParkingZones => Set<ParkingZone>();
    public DbSet<Session> Sessions => Set<Session>();
    public DbSet<Payment> Payments => Set<Payment>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // PostGIS: геометрия зоны.
        modelBuilder.Entity<ParkingZone>()
            .Property(z => z.Geometry)
            .HasColumnType("geometry");
        modelBuilder.Entity<ParkingZone>()
            .HasIndex(z => z.Name)
            .IsUnique();
        modelBuilder.Entity<Session>()
            .HasIndex(s => new { s.UserId, s.Status });
        modelBuilder.Entity<Payment>()
            .HasIndex(p => p.SessionId)
            .IsUnique();

        base.OnModelCreating(modelBuilder);
    }
}
