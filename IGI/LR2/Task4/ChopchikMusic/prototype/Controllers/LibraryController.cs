using MediatR;
using Microsoft.AspNetCore.Mvc;
using prototype.Service.AlbumUseCases.Commands;
using prototype.Service.AlbumUseCases.Queries;
using prototype.Service.PlaylistUseCases.Commands;
using prototype.Service.PlaylistUseCases.Queries;
using prototype.Service.SongUseCases.Commands;
using prototype.Service.SongUseCases.Queries;

namespace prototype.Controllers
{
	public class LibraryController : Controller
    {
        private readonly IMediator _mediator;

        public LibraryController(IMediator mediator)
        {
            _mediator = mediator;
        }

        [HttpPost]
        public async Task<IActionResult> UploadMusic(IFormFile musicFile, string authorName, string albumName, string songTitle) {

            var result = await _mediator.Send(new AddSongCommand(songTitle, authorName, albumName, musicFile));
            if (result.StatusCode==200) {
                return Json(result.Description);
            }
            else return BadRequest(result.Description);
        }
        //bebebe

        [HttpPost]
        public async Task<IActionResult> CreateAlbum(string title, string genre, string author) {
            var result = await _mediator.Send(new AddAlbumCommand(title, author, genre));
            if (result.StatusCode == 200)
            {
                return Json(result.Data);
            }
            else return BadRequest(result.Description);
        }

        [HttpGet]
        public async Task<IActionResult> GetPlaylistsByUser(int id)
        {
            var result = await _mediator.Send(new GetPlaylistByIdQuery(id));
            if (result.StatusCode == 200)
            {
                return Json(result.Data);
            }
            else
            {
                return BadRequest(result.Description);
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetSongsByPlaylist(int id)
        {
            var result = await _mediator.Send(new GetSongByPlaylistIdQuery(id));
            if (result.StatusCode == 200)
            {
                return Json(result.Data);
            }
            else
            {
                return BadRequest(result.Description);
            }
        }

        [HttpPut]
        public async Task<IActionResult> AddPlaylist(int userId, string name, string path = "newPlaylist.jpg")
        {
            var result = await _mediator.Send(new AddPlaylistCommand(name, path, userId));
            if (result.StatusCode==200)
            {
                return Json(result.Data);
            }
            else
            {
                return BadRequest(result.Description);
            }
        }
        
        [HttpGet]
        public async Task<IActionResult> GetFavouriteSongs(int id)
        {
            var result = await _mediator.Send(new GetFavouriteSongsByUserId(id));
            if (result.StatusCode == 200)
            {
                return Json(result.Data);
            }
            else
            {
                return BadRequest(result.Description);
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetAudio(string pathToSong)
        {
            pathToSong = "/Users/rinatbaitasov/Rinat/Univers/OOP/Music/" + pathToSong;
            var fileStream = new FileStream(pathToSong, FileMode.Open, FileAccess.Read);    
            return new FileStreamResult(fileStream, "audio/mpeg");
        }

        [HttpGet]
        public async Task<IActionResult> GetImage(string pathToImage)
        {
            pathToImage = "/Users/rinatbaitasov/Rinat/Univers/OOP/Image/" + pathToImage;
            var fileStream = new FileStream(pathToImage, FileMode.Open, FileAccess.Read);
            return new FileStreamResult(fileStream, "image/jpg");
        }

        [HttpGet]
        public async Task<IActionResult> FindSongByName(string name)
        {
            var result = await _mediator.Send(new GetSongsByNameQuery(name));
            if (result.StatusCode==200)
            {
                return Json(result);
            }
            else
            {
                return BadRequest(result.Description);
            }
        }

        [HttpPut]
        public async Task<IActionResult> AddSongToFavouriteSongs(int userId, int songId) {
            var result = await _mediator.Send(new AddFavouriteSongCommand(userId, songId));
            if (result.StatusCode==200) {
                return Json(result);
            }
            else {
                return BadRequest(result.Description);
            }
        }

        [HttpPut]
        public async Task<IActionResult> AddSongToPlaylist(int playlistId, int songId) {
            var result = await _mediator.Send(new AddSongToPlaylistCommand(playlistId, songId));
            if (result.StatusCode==200) {
                return Json(result);
            }
            else {
                return BadRequest(result.Description);
            }
        }

        // [HttpDelete]
        // public async Task<IActionResult> DeletePlaylist(int id) {
        //     var result = await _mediator.Send(new DeletePlaylistByIdCommand(id));
        // }

    }
}

