using Microsoft.EntityFrameworkCore;
using test2.Core.Data;

namespace test2.Core.Database;

public class AppDbContext : DbContext
{
    public DbSet<Book> Books { get; set; }
    public DbSet<Author> Authors { get; set; }
    public DbSet<Genre> Genres { get; set; }
    public DbSet<PublishingHouse> PublishingHouses { get; set; }
    public DbSet<BookAuthor> BookAuthors { get; set; }
    public DbSet<BookGenre> BookGenres { get; set; }

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
        
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Book>()
            .HasKey(x => x.IdBook);
        
        modelBuilder.Entity<PublishingHouse>()
            .HasKey(x => x.IdPublishingHouse);
        
        modelBuilder.Entity<Author>()
            .HasKey(x => x.IdAuthor);
        
        modelBuilder.Entity<Genre>()
            .HasKey(x => x.IdGenre);
        
        modelBuilder.Entity<Book>()
            .HasOne<PublishingHouse>()
            .WithMany()
            .HasForeignKey(x => x.IdPublishingHouse)
            .OnDelete(DeleteBehavior.Cascade);
        
        modelBuilder.Entity<BookAuthor>()
            .HasKey(x => new {x.IdBook, x.IdAuthor});
        
        modelBuilder.Entity<BookAuthor>()
            .HasOne<Book>()
            .WithMany()
            .HasForeignKey(x => x.IdBook)
            .OnDelete(DeleteBehavior.Cascade);
        
        modelBuilder.Entity<BookAuthor>()
            .HasOne<Author>()
            .WithMany()
            .HasForeignKey(x => x.IdAuthor)
            .OnDelete(DeleteBehavior.Cascade);
        
        modelBuilder.Entity<BookGenre>()
            .HasKey(x => new {x.IdGenre, x.IdBook});
        
        modelBuilder.Entity<BookGenre>()
            .HasOne<Genre>()
            .WithMany()
            .HasForeignKey(x => x.IdGenre)
            .OnDelete(DeleteBehavior.Cascade);
        
        modelBuilder.Entity<BookGenre>()
            .HasOne<Book>()
            .WithMany()
            .HasForeignKey(x => x.IdBook)
            .OnDelete(DeleteBehavior.Cascade);
        
        base.OnModelCreating(modelBuilder);
        
        modelBuilder.Entity<Author>().HasData(
            new Author { IdAuthor = 1, FirstName = "Gregory", LastName = "House"},
            new Author { IdAuthor = 2, FirstName = "Will", LastName = "Turner"}
        );
        
    }
    
}
