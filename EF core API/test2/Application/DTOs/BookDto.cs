namespace test2.Application.DTOs;

public class BookDto
{
    public required string Name { get; set; } = string.Empty;
    public required int IdPublishingHouse { get; set; }
    public required List<GenreDto> Genres { get; set; }
    public required List<int> Authors { get; set; }
    public required DateTime ReleaseDate { get; set; }
}
