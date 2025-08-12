namespace test2.Application.DTOs;

public class GetGenreDto
{
    public required int IdGenre { get; set; }
    public required string Name { get; set; } = string.Empty;
}