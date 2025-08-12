using Microsoft.EntityFrameworkCore;
using test2.Application.DTOs;
using test2.Application.Exceptions;
using test2.Application.Services.Abstractions;
using test2.Core.Data;
using test2.Core.Database;

namespace test2.Application.Services;

public class BookService : IBookService
{
    private readonly AppDbContext _dbContext;
    
    public BookService(AppDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<bool> PublishingHouseExistsAsync(int idPublishingHouse)
    {
        var publishingHouse = await _dbContext.PublishingHouses.FirstOrDefaultAsync(x => x.IdPublishingHouse == idPublishingHouse);
        return publishingHouse is not null;
    }

    public async Task<bool> AuthorExistsAsync(int idAuthor)
    {
        var author = await _dbContext.Authors.FirstOrDefaultAsync(x => x.IdAuthor == idAuthor);
        return author is not null;
    }

    public async Task<bool> GenreExistsAsync(int dGenre)
    {
        var genre = await _dbContext.Genres.FirstOrDefaultAsync(x => x.IdGenre == dGenre);
        return genre is not null;
    }

    public async Task<int> CreateBookAsync(BookDto bookDto)
    {
        foreach (var genre in bookDto.Genres)
        {
            if (!await GenreExistsAsync(genre.IdGenre))
            {
                var newGenre = new Genre()
                {
                    Name = genre.Name
                };
                _dbContext.Genres.Add(newGenre);
                await _dbContext.SaveChangesAsync();
            }
        }

        if (!await PublishingHouseExistsAsync(bookDto.IdPublishingHouse))
        {
            throw new PublishingHouseDoesNotExistException(bookDto.IdPublishingHouse);       
        }

        var newBook = new Book()
        {
            Name = bookDto.Name,
            ReleaseDate = bookDto.ReleaseDate,
            IdPublishingHouse = bookDto.IdPublishingHouse
        };
        
        _dbContext.Books.Add(newBook);
        await _dbContext.SaveChangesAsync();

        foreach (var authorId in bookDto.Authors)
        {
            
            if (!await AuthorExistsAsync(authorId))
            {
                throw new AuthorDoesNotExistException(authorId);
            }
            
            var newBookAuthor = new BookAuthor()
            {
                IdAuthor = authorId,
                IdBook = newBook.IdBook
            };
            _dbContext.BookAuthors.Add(newBookAuthor);
            await _dbContext.SaveChangesAsync();
        }

        foreach (var genre in bookDto.Genres)
        {
            var newBookGenre = new BookGenre()
            {
                IdGenre = genre.IdGenre,
                IdBook = newBook.IdBook
            };
            _dbContext.BookGenres.Add(newBookGenre);
            await _dbContext.SaveChangesAsync();
        }
        
        return newBook.IdBook;
        
    }
}
