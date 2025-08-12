namespace test2.Application.DTOs;

public class GetBookDto
{
    public required int IdBook { get; set; }
    public required string Name { get; set; } = string.Empty;
    public required List<GetAuthorDto> Authors { get; set; }
    public required List<GetGenreDto> Genres { get; set; }
    public required DateTime ReleaseDate { get; set; }
}
