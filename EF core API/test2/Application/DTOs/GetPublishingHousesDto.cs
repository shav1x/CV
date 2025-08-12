namespace test2.Application.DTOs;

public class GetPublishingHousesDto
{
    public required int IdPublishingHouse { get; set; }
    public required string Name { get; set; } = string.Empty;
    public required string Country { get; set; }
    public required string City { get; set; }
    public required List<GetBookDto> Books { get; set; } = [];
}