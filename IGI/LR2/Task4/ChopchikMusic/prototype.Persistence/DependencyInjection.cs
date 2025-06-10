using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using prototype.Persistence.Data;
using prototype.Persistence.Repository;

namespace prototype.Persistence
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddPersistence(this IServiceCollection
        services)
        {
            services.AddSingleton<IUnitOfWork, EfUnitOfWork>();
            return services;
        }
        public static IServiceCollection AddPersistence(
        this IServiceCollection services,
        DbContextOptions options)
        {
            services.AddPersistence()
            .AddSingleton<AppDbContext>(
            new AppDbContext((DbContextOptions<AppDbContext>)options));
            return services;
        }
    }
}

