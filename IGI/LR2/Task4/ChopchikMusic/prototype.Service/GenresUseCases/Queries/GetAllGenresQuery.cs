using System;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Queries
{
	public class GetAllGenresQuery : IRequest<BaseResponse<IEnumerable<Genre>>>
	{
		public GetAllGenresQuery()
		{
		}
	}
}

