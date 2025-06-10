using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
    public class GetSongByPlaylistIdQueryHandler : IRequestHandler<GetSongByPlaylistIdQuery, BaseResponse<IEnumerable<Song>>>
	{
        private readonly IUnitOfWork _unitOfWork;
        public GetSongByPlaylistIdQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IEnumerable<Song>>> Handle(GetSongByPlaylistIdQuery request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<PlaylistSong, bool>> filter = c => c.PlaylistId == request.Id;
                var playlistSongs = await _unitOfWork.PlaylistSongRepository.ListAsync(filter, cancellationToken);
                List<Song> songs = new List<Song>();
                foreach (var song in playlistSongs)
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
            catch (Exception ex)
            {
                return new BaseResponse<IEnumerable<Song>>()
                {
                    Description = ex.Message,
                    StatusCode = 500
                };
            }
        }
    }
}

