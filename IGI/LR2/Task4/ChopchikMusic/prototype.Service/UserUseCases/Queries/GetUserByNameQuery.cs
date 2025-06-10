using System;
using prototype.Domain;
using System.Security.Claims;

namespace prototype.Service.UserUseCases.Queries
{
	public class GetUserByNameQuery : IRequest<BaseResponse<ClaimsIdentity>>
	{
		public string Name { get; set; }
		public string Password { get; set; }
		public GetUserByNameQuery(string name, string pass)
		{
			Password = pass;
			Name = name;
		}
	}
}

