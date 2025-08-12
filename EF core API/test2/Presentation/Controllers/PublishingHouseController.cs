using Microsoft.AspNetCore.Mvc;
using test2.Application.DTOs;
using test2.Application.Services.Abstractions;

namespace test2.Presentation.Controllers;

[ApiController]
[Route("api/publishinghouse")]
public class PublishingHouseController(IPublishingHouseService publishingHouseService) : ControllerBase
{
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<GetPublishingHousesDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetPublishingHouses()
    {
        var publishingHouses = await publishingHouseService.GetAllPublishingHousesAsync();
        return Ok(publishingHouses);
    }
}
