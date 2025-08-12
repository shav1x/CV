namespace test2.Application.Exceptions;

public class AuthorDoesNotExistException(int id) : Exception($"Author with id {id} does not exist");