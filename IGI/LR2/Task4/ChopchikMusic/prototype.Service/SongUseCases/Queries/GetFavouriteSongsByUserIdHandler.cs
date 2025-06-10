using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
    public class GetFavouriteSongsByUserIdHandler : IRequestHandler<GetFavouriteSongsByUserId, BaseResponse<IEnumerable<Song>>>
	{

        private readonly IUnitOfWork _unitOfWork;

		public GetFavouriteSongsByUserIdHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IEnumerable<Song>>> Handle(GetFavouriteSongsByUserId request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<UserFavouriteSong, bool>> filter = c => c.UserId == request.Id;
                var favouriteSongs = await _unitOfWork.UserFavouriteSongRepository.ListAsync(filter, cancellationToken);
                List<Song> songs = new List<Song>();
                foreach (var song in favouriteSongs)
                {
                    var _song = await _unitOfWork.SongRepository.GetByIdAsync(song.SongId);
                    songs.Add(_song);
                }
                return new BaseResponse<IEnumerable<Song>>()
                {
                    StatusCode = 200,
                    Data = songs
                };
            }
            catch(Exception ex)
            {
                return new BaseResponse<IEnumerable<Song>>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

