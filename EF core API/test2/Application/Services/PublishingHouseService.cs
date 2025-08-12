using Microsoft.EntityFrameworkCore;
using test2.Application.DTOs;
using test2.Application.Services.Abstractions;
using test2.Core.Database;

namespace test2.Application.Services;

public class PublishingHouseService : IPublishingHouseService
{
    private readonly AppDbContext _dbContext;
    
    public PublishingHouseService(AppDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<List<GetPublishingHousesDto>> GetAllPublishingHousesAsync()
    {
        var publishingHousesList = new List<GetPublishingHousesDto>();
        var publishingHousesAsync = await _dbContext.PublishingHouses.ToListAsync();
        foreach (var publishingHouse in publishingHousesAsync)
        {
            var books = await _dbContext.Books
                .Where(b => b.IdPublishingHouse == publishingHouse.IdPublishingHouse)
                .Select(b => new GetBookDto()
                {
                    IdBook = b.IdBook,
                    Name = b.Name,
                    Authors = _dbContext.BookAuthors
                        .Where(ba => ba.IdBook == b.IdBook)
                        .Join(_dbContext.Authors,
                            ba => ba.IdAuthor,
                            a => a.IdAuthor,
                            (ba, a) => new GetAuthorDto()
                            {
                                IdAuthor = a.IdAuthor,
                                FirstName = a.FirstName,
                                LastName = a.LastName
                            }).ToList(),
                    Genres = _dbContext.BookGenres
                        .Where(bg => bg.IdBook == b.IdBook)
                        .Join(_dbContext.Genres,
                            bg => bg.IdGenre,
                            g => g.IdGenre,
                            (bg, g) => new GetGenreDto()
                            {
                                IdGenre = g.IdGenre,
                                Name = g.Name
                            }).ToList(),
                    ReleaseDate = b.ReleaseDate
                }).ToListAsync();
            var publishingHouseDto = new GetPublishingHousesDto()
            {
                IdPublishingHouse = publishingHouse.IdPublishingHouse,
                Name = publishingHouse.Name,
                Country = publishingHouse.Country,
                City = publishingHouse.City,
                Books = books
            };
            publishingHousesList.Add(publishingHouseDto);
        }
        return publishingHousesList;
    }
}
