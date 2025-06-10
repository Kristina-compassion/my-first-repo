using System;
namespace prototype.Domain.Entities
{
	public class Song : Entity
	{		
		public string Name { get; set; }
		public string PathToImage { get; set; }
		public string PathToSong { get; set; }
		public int AlbumId { get; set; }
		public Album Album { get; set; }

		public Song()
		{

		}

		public Song(string name, string pathToImage, string pathToSong, int albumId, Album album)
		{
			Name = name;
			PathToImage = pathToImage;
			PathToSong = pathToSong;
			Album = album;
			AlbumId = albumId;
		}

	}
}

