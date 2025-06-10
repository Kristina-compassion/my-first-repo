using System;
namespace prototype.Domain.Entities
{
	public class PlaylistUser : Entity
	{
		public int UserId { get; set; }
		public User User { get; set; }

		public int PlaylistId { get; set; }
		public Playlist Playlist { get; set; }

		public PlaylistUser()
		{
			UserId = 0;
			User = new User();
			PlaylistId = 0;
			Playlist = new Playlist();
		}

		public PlaylistUser(int userId, User user, int playlistId, Playlist playlist)
		{
			UserId = userId;
			User = user;
			PlaylistId = playlistId;
			Playlist = playlist;
		}
	}
}

