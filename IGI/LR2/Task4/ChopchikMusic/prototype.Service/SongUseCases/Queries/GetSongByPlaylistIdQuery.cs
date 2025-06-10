using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
	public class GetSongByPlaylistIdQuery : IRequest<BaseResponse<IEnumerable<Song>>>
	{
		public int Id { get; set; }
		public GetSongByPlaylistIdQuery(int id)
		{
			Id = id;
		}
	}
}

