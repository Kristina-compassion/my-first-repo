using System;
using Microsoft.AspNetCore.Http;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddSongCommand : IRequest<BaseResponse<Song>>
	{
            public string Name{get;set;}
            public string AuthorName {get;set;}
            public string AlbumName {get;set;}
            public IFormFile File {get;set;}

            public AddSongCommand(string name, string author, string album, IFormFile file)
            {
                  Name = name;
                  AuthorName = author;
                  AlbumName = album;
                  File = file;
            }
	}
}

