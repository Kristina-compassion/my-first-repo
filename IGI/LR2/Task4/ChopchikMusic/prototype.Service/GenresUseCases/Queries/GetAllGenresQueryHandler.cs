using System;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Queries
{
    public class GetAllGenresQueryHandler : IRequestHandler<GetAllGenresQuery, BaseResponse<IEnumerable<Genre>>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public GetAllGenresQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IEnumerable<Genre>>> Handle(GetAllGenresQuery request, CancellationToken cancellationToken)
        {
            try
            {
                var genres = await _unitOfWork.GenreRepository.ListAllAsync();
                return new BaseResponse<IEnumerable<Genre>>()
                {
                    StatusCode = 200,
                    Data = genres
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<IEnumerable<Genre>>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

