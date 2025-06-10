using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
	public class GetSongsByAlbumIdCommand : IRequest<BaseResponse<IReadOnlyList<Song>>>
	{
		public int AlbumId { get; set; }
		public GetSongsByAlbumIdCommand(int id)
		{
			AlbumId = id;
		}
	}
}

