using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Queries
{
	public class GetAlbumsByAuthorQueryHandler : IRequestHandler<GetAlbumsByAuthorQuery, BaseResponse<IEnumerable<Album>>>
    {
        private readonly IUnitOfWork _unitOfWork;

		public GetAlbumsByAuthorQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IEnumerable<Album>>> Handle(GetAlbumsByAuthorQuery request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<AlbumAuthor, bool>> filter = c => c.AuthorId == request.AuthorId;
                var albumsAuthor = await _unitOfWork.AlbumAuthorRepository.ListAsync(filter, cancellationToken);
                List<Album> albums = new List<Album>();
                foreach (var album in albumsAuthor)
                {
                    albums.Add(album.Album);
                }
                return new BaseResponse<IEnumerable<Album>>()
                {
                    StatusCode = 200,
                    Data = albums
                };
            }
            catch(Exception ex)
            {
                return new BaseResponse<IEnumerable<Album>>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

