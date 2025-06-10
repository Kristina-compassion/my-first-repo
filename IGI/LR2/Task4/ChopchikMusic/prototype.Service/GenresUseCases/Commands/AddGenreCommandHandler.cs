using System;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Commands
{
    public class AddGenreCommandHandler : IRequestHandler<AddGenreCommand, BaseResponse<Genre>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public AddGenreCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Genre>> Handle(AddGenreCommand request, CancellationToken cancellationToken)
        {
            try
            {
                Genre genre = new Genre(request.Name);
                await _unitOfWork.GenreRepository.AddAsync(genre);
                return new BaseResponse<Genre>()
                {
                    StatusCode = 200,
                    Data = genre
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<Genre>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

