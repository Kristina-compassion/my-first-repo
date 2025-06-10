using System;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Queries
{
	public class GetAlbumByNameQuery : IRequest<BaseResponse<Album>>
	{
		public string Name { get; set; }
		public GetAlbumByNameQuery(string name)
		{
			Name = name;
		}
	}
}

