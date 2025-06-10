using System;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddFavouriteSongCommandHandler : IRequestHandler<AddFavouriteSongCommand, BaseResponse<Song>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public AddFavouriteSongCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Song>> Handle(AddFavouriteSongCommand request, CancellationToken cancellationToken)
        {
            try
            {
                var user = await _unitOfWork.UserRepository.GetByIdAsync(request.UserId);
                var song = await _unitOfWork.SongRepository.GetByIdAsync(request.SongId);
                var favouriteSong = new UserFavouriteSong(request.SongId, song, request.UserId, user);
                await _unitOfWork.UserFavouriteSongRepository.AddAsync(favouriteSong);
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

