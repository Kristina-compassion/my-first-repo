using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
    public class GetSongsByAlbumIdCommandHandler : IRequestHandler<GetSongsByAlbumIdCommand, BaseResponse<IReadOnlyList<Song>>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public GetSongsByAlbumIdCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IReadOnlyList<Song>>> Handle(GetSongsByAlbumIdCommand request, CancellationToken cancellationToken)
        {
            try
            {                
                Expression<Func<Song, bool>> filter = c => c.AlbumId == request.AlbumId;
                var songs = await _unitOfWork.SongRepository.ListAsync(filter, cancellationToken);
                return new BaseResponse<IReadOnlyList<Song>>()
                {
                    StatusCode = 200,
                    Data = songs
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<IReadOnlyList<Song>>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

