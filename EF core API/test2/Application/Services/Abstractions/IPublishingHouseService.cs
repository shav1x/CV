using test2.Application.DTOs;

namespace test2.Application.Services.Abstractions;

public interface IPublishingHouseService
{
    Task<List<GetPublishingHousesDto>> GetAllPublishingHousesAsync();
}