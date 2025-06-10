using System;
namespace prototype.Domain.Entities
{
	public class UserFavouriteAuthor : Entity
	{
		public int UserId { get; set; }
		public User User { get; set; }

		public int AuthorId { get; set; }
		public User Author { get; set; }

		public UserFavouriteAuthor()
		{
			UserId = 0;
			AuthorId = 0;
			User = new User();
			Author = new User();
		}

		public UserFavouriteAuthor(int userId, User user, int authorId, User author)
		{
			UserId = userId;
			User = user;
			AuthorId = authorId;
			Author = author;
		}
	}
}

