namespace test2.Application.Exceptions;

public class PublishingHouseDoesNotExistException(int id) : Exception($"Publishing house with id {id} does not exist");
