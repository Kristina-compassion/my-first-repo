using System;
using System.Security.Claims;
using prototype.Domain;

namespace prototype.Service.UserUseCases.Commands
{
	public class AddUserCommand : IRequest<BaseResponse<ClaimsIdentity>>
    {
		public string Name { get; set; }
		public string Password { get; set; }
		public string Email { get; set; }
		public string Role { get; set; }
		public string PathToImage { get; set; }

		public AddUserCommand(string name, string email, string pass, string role, string path)
		{
			Name = name;
			Password = pass;
			Email = email;
			Role = role;
			PathToImage = path;
		}
	}
}

