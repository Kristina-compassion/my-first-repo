using System;
namespace prototype.Domain.Entities
{
	public class Playlist : Entity
	{
		public string Name { get; set; }
		public string PathToImage { get; set; }
		public int UserId { get; set; }
		public User User { get; set; }

		public Playlist()
		{
			Name = "";
			PathToImage = "";
		}

		public Playlist(string name, string path, int userId, User user)
		{
			Name = name;
			PathToImage = path;
			UserId = userId;
			User = user;
		}

	}
}

