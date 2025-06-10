using System;
namespace prototype.Domain.Entities
{
	public class UserFavouriteSong : Entity
	{
		public int SongId { get; set; }
		public Song Song { get; set; }

		public int UserId { get; set; }
		public User User { get; set; }

		public UserFavouriteSong()
		{
			SongId = 0;
			Song = new Song();
			UserId = 0;
			User = new User();
		}

		public UserFavouriteSong(int songId, Song song, int userId, User user)
		{
			SongId = songId;
			Song = song;
			UserId = userId;
			User = user;
		}

	}
}

