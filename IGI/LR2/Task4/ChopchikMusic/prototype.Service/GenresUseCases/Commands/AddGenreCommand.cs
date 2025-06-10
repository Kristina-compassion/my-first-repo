using System;
using prototype.Domain;

namespace prototype.Service.GenresUseCases.Commands
{
	public class AddGenreCommand : IRequest<BaseResponse<Genre>>
	{
		public string Name { get; set; }
		public AddGenreCommand(string name)
		{
			Name = name;
		}
	}
}

