using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Queries
{
	public class GetAlbumByNameQueryHandler : IRequestHandler<GetAlbumByNameQuery, BaseResponse<Album>>
    {
        private readonly IUnitOfWork _unitOfWork;

		public GetAlbumByNameQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Album>> Handle(GetAlbumByNameQuery request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<Album, bool>> filter = c => c.Name == request.Name;
                var albums = await _unitOfWork.AlbumRepository.ListAsync(filter, cancellationToken);
                var album = albums[0];
                return new BaseResponse<Album>()
                {
                    StatusCode = 200,
                    Data = album
                };
            }
            catch(Exception ex)
            {
                return new BaseResponse<Album>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

