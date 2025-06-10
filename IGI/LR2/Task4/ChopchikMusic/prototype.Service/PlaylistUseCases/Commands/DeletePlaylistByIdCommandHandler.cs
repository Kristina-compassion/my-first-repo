using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.PlaylistUseCases.Commands
{
	public class DeletePlaylistByIdCommandHandler : IRequestHandler<DeletePlaylistByIdCommand, BaseResponse<bool>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public DeletePlaylistByIdCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<bool>> Handle(DeletePlaylistByIdCommand request, CancellationToken cancellationToken)
        {
            try
            {
                var playlist = await _unitOfWork.PlaylistRepository.GetByIdAsync(request.Id);
                Expression <Func<PlaylistSong, bool> > filter = c => c.PlaylistId==request.Id;
                var playlistsongs = await _unitOfWork.PlaylistSongRepository.ListAsync(filter, cancellationToken);
                foreach (var plist in playlistsongs) {
                    await _unitOfWork.PlaylistSongRepository.DeleteAsync(plist, cancellationToken);
                }
                await _unitOfWork.PlaylistRepository.DeleteAsync(playlist);
                return new BaseResponse<bool>()
                {
                    StatusCode = 200,
                    Data = true
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<bool>()
                {
                    StatusCode = 500,
                    Data = false,
                    Description = ex.Message
                };
            }
        }
    }
}

