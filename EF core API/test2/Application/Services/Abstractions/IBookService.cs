using test2.Application.DTOs;
using test2.Core.Data;

namespace test2.Application.Services.Abstractions;

public interface IBookService
{
    Task<bool> PublishingHouseExistsAsync(int idPublishingHouse);
    Task<bool> AuthorExistsAsync(int idAuthor);
    Task<bool> GenreExistsAsync(int idGenre);
    Task<int> CreateBookAsync(BookDto bookDto);
}
