using System;
using System.Linq.Expressions;
using prototype.Domain;
using System.Security.Claims;
using prototype.Domain.Entities;

namespace prototype.Service.UserUseCases.Queries
{
	public class GetUserByNameQueryHandler : IRequestHandler<GetUserByNameQuery, BaseResponse<ClaimsIdentity>>
	{
        private readonly IUnitOfWork _unitOfWork;

		public GetUserByNameQueryHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<ClaimsIdentity>> Handle(GetUserByNameQuery request, CancellationToken cancellationToken)
        {
            Expression<Func<User, bool>> filter = c => c.Name == request.Name;
            var users = await _unitOfWork.UserRepository.ListAsync(filter, cancellationToken);
            if (users.Count==0)
            {
                return new BaseResponse<ClaimsIdentity>()
                {
                    Description = "I have no users with the login",
                    StatusCode = 400
                };
            }
            if (users[0].Password == request.Password)
            {
                var result = AuthenticateService.Authenticate(users[0]);
                return new BaseResponse<ClaimsIdentity>()
                {
                    Data = result,
                    StatusCode = 200
                };
            }
            else return new BaseResponse<ClaimsIdentity>()
            {
                Description = "Invalid login or password",
                StatusCode = 400
            };
        }
    }
}

