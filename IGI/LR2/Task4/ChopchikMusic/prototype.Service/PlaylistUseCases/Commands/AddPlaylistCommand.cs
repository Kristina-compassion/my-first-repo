using System;
using prototype.Domain;

namespace prototype.Service.PlaylistUseCases.Commands
{
	public class AddPlaylistCommand : IRequest<BaseResponse<Playlist>>
	{
		public string Name { get; set; }
		public string PathToImage { get; set; }
		public int UserId { get; set; }

		public AddPlaylistCommand(string name, string path, int userId)
		{
			Name = name;
			PathToImage = path;
			UserId = userId;
		}
	}
}

