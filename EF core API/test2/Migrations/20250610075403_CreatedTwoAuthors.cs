using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace test2.Migrations
{
    /// <inheritdoc />
    public partial class CreatedTwoAuthors : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.InsertData(
                table: "Authors",
                columns: new[] { "IdAuthor", "FirstName", "LastName" },
                values: new object[,]
                {
                    { 1, "Gregory", "House" },
                    { 2, "Will", "Turner" }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "Authors",
                keyColumn: "IdAuthor",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Authors",
                keyColumn: "IdAuthor",
                keyValue: 2);
        }
    }
}
