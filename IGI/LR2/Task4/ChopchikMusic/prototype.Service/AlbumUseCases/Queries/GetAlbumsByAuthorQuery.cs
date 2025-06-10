using System;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Queries
{
	public class GetAlbumsByAuthorQuery : IRequest<BaseResponse<IEnumerable<Album>>>
	{
		public int AuthorId { get; set; }
		public GetAlbumsByAuthorQuery(int authorId)
		{
			AuthorId = authorId;
		}
	}
}

