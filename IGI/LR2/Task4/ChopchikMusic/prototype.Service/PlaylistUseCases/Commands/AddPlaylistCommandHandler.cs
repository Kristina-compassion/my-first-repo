using System;
using prototype.Domain;

namespace prototype.Service.PlaylistUseCases.Commands
{
	public class AddPlaylistCommandHandler : IRequestHandler<AddPlaylistCommand, BaseResponse<Playlist>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public AddPlaylistCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Playlist>> Handle(AddPlaylistCommand request, CancellationToken cancellationToken)
        {
            try
            {
                var user = await _unitOfWork.UserRepository.GetByIdAsync(request.UserId);
                Playlist playlist = new Playlist(request.Name, request.PathToImage, request.UserId, user);
                await _unitOfWork.PlaylistRepository.AddAsync(playlist);
                return new BaseResponse<Playlist>()
                {
                    StatusCode = 200,
                    Data = playlist
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<Playlist>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

