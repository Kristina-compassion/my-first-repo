using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Queries
{
    public class GetFavouriteGenresQueryHandler : IRequestHandler<GetFavouriteGenresQuery, BaseResponse<IEnumerable<Genre>>>
	{
        private readonly IUnitOfWork _unitOfWork;
        public GetFavouriteGenresQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IEnumerable<Genre>>> Handle(GetFavouriteGenresQuery request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<UserFavouriteGenres, bool>> filter = c => c.UserId == request.UserId;
                var favouriteGenres = await _unitOfWork.UserFavouriteGenresRepository.ListAsync(filter, cancellationToken);
                var genres = new List<Genre>();
                foreach (var genre in favouriteGenres)
                {
                    genres.Add(genre.Genre);
                }
                return new BaseResponse<IEnumerable<Genre>>()
                {
                    StatusCode = 200,
                    Data = genres
                };
            }
            catch(Exception ex)
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

