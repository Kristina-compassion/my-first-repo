using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddFavouriteSongCommand : IRequest<BaseResponse<Song>>
	{
		public int UserId { get; set; }
		public int SongId { get; set; }
		public AddFavouriteSongCommand(int userId, int songId)
		{
			UserId = userId;
			SongId = songId;
		}
	}
}

