using System;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Queries
{
	public class GetFavouriteGenresQuery : IRequest<BaseResponse<IEnumerable<Genre>>>
	{
		public int UserId { get; set; }
		public GetFavouriteGenresQuery(int userId)
		{
			UserId = userId;
		}
	}
}

