using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.SongUseCases.Commands
{
	public class AddSongCommandHandler : IRequestHandler<AddSongCommand, BaseResponse<Song>>
	{

        private readonly IUnitOfWork _unitOfWork;
		public AddSongCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Song>> Handle(AddSongCommand request, CancellationToken cancellationToken)
        {
            try
            {                
                Expression <Func<Album, bool> > filter = c => c.Name == request.AlbumName;
                var albums = await _unitOfWork.AlbumRepository.ListAsync(filter, cancellationToken);
                Album album = albums[0];

                Song song = new Song(request.Name, "Herman.jpg", "", album.Id, album); 
                await _unitOfWork.SongRepository.AddAsync(song, cancellationToken);
                await _unitOfWork.SaveAllAsync();
                int songId = song.Id;
                string pathToSong = $"/Users/rinatbaitasov/Rinat/Univers/OOP/Music/{songId}.mp3";
                using (var stream = new FileStream(pathToSong, FileMode.Create))
                {
                    await request.File.CopyToAsync(stream);
                }

                song.PathToSong = $"{songId}.mp3";
                await _unitOfWork.SaveAllAsync();

                Expression<Func<User, bool>> filter2 = c => c.Name == request.AuthorName;
                var authors = await _unitOfWork.UserRepository.ListAsync(filter2, cancellationToken);
                User author = authors[0];
                SongAuthor songAuthor = new SongAuthor(song.Id, song, author.Id, author);
                await _unitOfWork.SongAuthorRepository.AddAsync(songAuthor, cancellationToken);

                ///DOP
                var playlists = await _unitOfWork.PlaylistRepository.ListAllAsync();
                var playlist = playlists[0];
                await _unitOfWork.PlaylistSongRepository.AddAsync(new PlaylistSong (playlist.Id, playlist, song.Id, song), cancellationToken);

                return new BaseResponse<Song>()
                {
                    StatusCode = 200,
                    Data = song
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<Song>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

