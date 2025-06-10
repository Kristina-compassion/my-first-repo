using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
	public class GetFavouriteSongsByUserId : IRequest<BaseResponse<IEnumerable<Song>>>
    {
		public int Id { get; set; }
		public GetFavouriteSongsByUserId(int id)
		{
			Id = id;
		}
	}
}

