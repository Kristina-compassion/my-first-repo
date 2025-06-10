using System;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Commands
{
	public class AddAlbumCommand : IRequest<BaseResponse<Album>>
	{
		public string Name { get; set; }
		public string AuthorName { get; set; }
		public string GenreName { get; set; }
		public AddAlbumCommand(string name, string author, string genre)
		{
			Name = name;
			AuthorName = author;
			GenreName = genre;
		}
	}
}

