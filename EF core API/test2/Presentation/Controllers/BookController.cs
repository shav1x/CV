using Microsoft.AspNetCore.Mvc;
using test2.Application.DTOs;
using test2.Application.Services.Abstractions;

namespace test2.Presentation.Controllers;

[ApiController]
[Route("api/book")]
public class BookController(IBookService bookService) : ControllerBase
{
    
    [HttpPost]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    [ProducesResponseType(StatusCodes.Status500InternalServerError)]
    public async Task<IActionResult> AddBook([FromBody] BookDto bookDto)
    {
        var bookId = await bookService.CreateBookAsync(bookDto);
        return CreatedAtAction(nameof(AddBook), new { bookId }, bookId);
    }
    
}
