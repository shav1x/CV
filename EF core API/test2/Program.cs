using Microsoft.EntityFrameworkCore;
using test2.Application;
using test2.Core.Database;

namespace test2;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.Services.AddControllers();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.AddApplicationServices();
        
        var conString = builder.Configuration.GetConnectionString("Postgres");
        builder.Services.AddDbContext<AppDbContext>(opt =>
        {
            opt.UseSqlServer(conString);
        });

        var app = builder.Build();
        
        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();

        app.UseAuthorization();
        
        var scope = app.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        db.Database.Migrate();
        
        app.MapControllers();

        app.Run();
    }
}
