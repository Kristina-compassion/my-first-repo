using System;
using prototype.Domain;

namespace prototype.Service.PlaylistUseCases.Commands {
    public class DeletePlaylistByIdCommand : IRequest<BaseResponse<bool>>
	{
		public int Id {get;set;}

		public DeletePlaylistByIdCommand(int id) {
            Id = id;
        }
	}
}