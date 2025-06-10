using System;
namespace prototype.Domain.Entities
{
	public class AlbumAuthor : Entity
	{
		public int AlbumId { get; set; }
		public Album Album { get; set; }

		public int AuthorId { get; set; }
		public User Author { get; set; }

		public AlbumAuthor()
		{
			AlbumId = 0;
			Album = new Album();
			AuthorId = 0;
			Author = new User();
		}

		public AlbumAuthor(int albumId, Album album, int authorId, User author)
		{
			AlbumId = albumId;
			Album = album;
			AuthorId = authorId;
			Author = author;
		}
	}
}

