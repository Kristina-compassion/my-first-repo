using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddSongToPlaylistCommand : IRequest<BaseResponse<Song>>
	{
		public int PlaylistId { get; set; }
		public int SongId { get; set; }
		public AddSongToPlaylistCommand(int playlistId, int songId)
		{
			PlaylistId = playlistId;
			SongId = songId;
		}
	}
}

