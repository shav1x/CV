namespace test2.Core.Data;

public class Book
{
    public int IdBook { get; set; }
    public required string Name { get; set; }
    public DateTime ReleaseDate { get; set; }
    public int IdPublishingHouse { get; set; }
}
