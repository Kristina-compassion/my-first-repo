using System;
namespace prototype.Domain.Entities
{
	public class UserFavouriteGenres : Entity
	{
		public int UserId { get; set; }
		public User User { get; set; }

		public int GenreId { get; set; }
		public Genre Genre { get; set; }

		public UserFavouriteGenres()
		{
			UserId = 0;
			GenreId = 0;
			User = new User();
			Genre = new Genre();
		}

		public UserFavouriteGenres(int userId, User user, int genreId, Genre genre)
		{
			UserId = userId;
			User = user;
			GenreId = genreId;
			Genre = genre;
		}
	}
}

