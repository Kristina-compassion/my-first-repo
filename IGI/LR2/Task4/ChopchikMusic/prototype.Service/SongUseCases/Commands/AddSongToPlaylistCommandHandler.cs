using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddSongToPlaylistHandler : IRequestHandler<AddSongToPlaylistCommand, BaseResponse<Song>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public AddSongToPlaylistHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Song>> Handle(AddSongToPlaylistCommand request, CancellationToken cancellationToken)
        {
            try
            {
                var playlist = await _unitOfWork.PlaylistRepository.GetByIdAsync(request.PlaylistId);
                var song = await _unitOfWork.SongRepository.GetByIdAsync(request.SongId);
                var playilstSong = new PlaylistSong(request.PlaylistId, playlist, request.SongId, song);
                await _unitOfWork.PlaylistSongRepository.AddAsync(playilstSong);
                return new BaseResponse<Song>()
                {
                    StatusCode = 200,
                    Data = song
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<Song>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

