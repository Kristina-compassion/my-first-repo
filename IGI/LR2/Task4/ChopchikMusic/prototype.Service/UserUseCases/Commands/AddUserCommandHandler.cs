using System;
using prototype.Domain;
using System.Security.Claims;
using System.Linq.Expressions;

namespace prototype.Service.UserUseCases.Commands
{
    public class AddUserCommandHandler : IRequestHandler<AddUserCommand, BaseResponse<ClaimsIdentity>>
	{
        private readonly IUnitOfWork _unitOfWork;

		public AddUserCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<ClaimsIdentity>> Handle(AddUserCommand request, CancellationToken cancellationToken)
        {
            User user = new User(request.Name, request.Email, request.Password, request.Role, request.PathToImage);

            try
            {
                Expression<Func<User, bool>> filter = c => c.Name == request.Name;
                var users = await _unitOfWork.UserRepository.ListAsync(filter);
                if (users.Count != 0)
                {
                    return new BaseResponse<ClaimsIdentity>()
                    {
                        Description = "Пользователь с таким именем уже существует",
                        StatusCode = 400
                    };
                }
                await _unitOfWork.UserRepository.AddAsync(user, cancellationToken);
                var result = AuthenticateService.Authenticate(user);
                return new BaseResponse<ClaimsIdentity>()
                {
                    Data = result,
                    StatusCode = 200
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<ClaimsIdentity>()
                {
                    Description = ex.Message,
                    StatusCode = 500
                };
            }
        }
    }
}

