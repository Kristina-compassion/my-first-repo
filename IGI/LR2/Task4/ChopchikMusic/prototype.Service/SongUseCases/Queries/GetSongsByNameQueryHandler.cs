using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Queries
{
	public class GetSongsByNameQueryHandler : IRequestHandler<GetSongsByNameQuery, BaseResponse<IReadOnlyList<Song>>>
	{

        private readonly IUnitOfWork _unitOfWork;

		public GetSongsByNameQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<IReadOnlyList<Song>>> Handle(GetSongsByNameQuery request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<Song, bool>> filter = c => c.Name == request.Name;
                var result = await _unitOfWork.SongRepository.ListAsync(filter, cancellationToken);
                return new BaseResponse<IReadOnlyList<Song>>()
                {
                    Data = result,
                    StatusCode = 200
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<IReadOnlyList<Song>>()
                {
                    Description = ex.Message,
                    StatusCode = 500
                };
            }
        }
    }
}

