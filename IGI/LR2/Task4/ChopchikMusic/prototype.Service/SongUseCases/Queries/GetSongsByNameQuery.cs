using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
	public class GetSongsByNameQuery : IRequest<BaseResponse<IReadOnlyList<Song>>>
    {
		public string Name { get; set; }
		public GetSongsByNameQuery(string name)
		{
			Name = name;
		}
	}
}

