using Microsoft.OpenApi;

var builder = WebApplication.CreateBuilder(args);

// Добавляем контроллеры и Swagger
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "Media Processing API", Version = "v1" });
});

// Регистрируем наши сервисы (из сгенерированного кода)
builder.Services.AddSingleton<MediaProcessingApi.Services.InMemoryStore>();
builder.Services.AddScoped<MediaProcessingApi.Services.ApplicationService>();
builder.Services.AddScoped<MediaProcessingApi.Services.FileService>();

var app = builder.Build();

// Включаем Swagger UI
app.UseSwagger();
app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "Media API v1"));

app.MapControllers();

app.Run();
