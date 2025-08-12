namespace test2.Application.DTOs;

public class GetAuthorDto
{
    public required int IdAuthor { get; set; }
    public required string FirstName { get; set; } = string.Empty;
    public required string LastName { get; set; } = string.Empty;
}