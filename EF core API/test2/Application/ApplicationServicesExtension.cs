using test2.Application.Services;
using test2.Application.Services.Abstractions;
using test2.Core.Database;

namespace test2.Application;

public static class ApplicationServicesExtension
{
    public static void AddApplicationServices(this IServiceCollection app)
    {
        app.AddScoped<IBookService, BookService>();
        app.AddScoped<IPublishingHouseService, PublishingHouseService>();
    }
}
