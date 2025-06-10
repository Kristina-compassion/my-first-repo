using System;
using Microsoft.Extensions.DependencyInjection;
using System.Numerics;

namespace prototype.Service
{
	public class DbInitializer
	{
        public static async Task Initialize(IServiceProvider services)
        {
            var unitOfWork = services.GetRequiredService<IUnitOfWork>();

            //await unitOfWork.DeleteDataBaseAsync();
            //await unitOfWork.CreateDataBaseAsync();
            await unitOfWork.ConnectDataBaseAsync();

            //public User(string? name, string? email, string? password, string? role, string? path)
            var user = new User("Три дня дождя", "prodalsya@gmail.com", "1234", "User", "Herman.jpg");
            await unitOfWork.UserRepository.AddAsync(user);

            ///Add the users
            //var user = new User("Admin", "admin", "1234", "Admin", "Herman.jpg");
            //await unitOfWork.UserRepository.AddAsync(user);

            //user = new User("Rinat", "rinat@puk.puk", "1111", "User", "Herman.jpg");
            //await unitOfWork.UserRepository.AddAsync(user);

            //var playlist = new Playlist("Test", "Herman.jpg", 2, user);
            //await unitOfWork.PlaylistRepository.AddAsync(playlist);

            //var playlistUser = new PlaylistUser(2, user, 1, playlist);
            //await unitOfWork.PlaylistUserRepository.AddAsync(playlistUser);

            //var genre = new Genre("Rock");
            //await unitOfWork.GenreRepository.AddAsync(genre);

            //var author = new User("Nirvana", "kurtKobbein@nevesa.bog", "dulo", "User", "Nirvana.jpg");
            //await unitOfWork.UserRepository.AddAsync(author);

            //var album = new Album("Nevermind", "Herman.jpg", 1, genre);
            //await unitOfWork.AlbumRepository.AddAsync(album);

            //var albumAuthor = new AlbumAuthor(1, album, 1, author);
            //await unitOfWork.AlbumAuthorRepository.AddAsync(albumAuthor);

            ///========================================================Nevermind

            /*

            var song = new Song("Smells like teen spirit", "Herman.jpg", "smellslike.mp3",1, album);
            await unitOfWork.SongRepository.AddAsync(song);

            var songAuthor = new SongAuthor(1, song, 1, author);
            await unitOfWork.SongAuthorRepository.AddAsync(songAuthor);

            var playlistSong = new PlaylistSong(1, playlist, 1, song);
            await unitOfWork.PlaylistSongRepository.AddAsync(playlistSong);

       

            ///========================================================три дня дождя

            author = new Author("Три дня дождя", "tdd.jpg");
            await unitOfWork.AuthorRepository.AddAsync(author);

            album = new Album("Байполар", "baipolar.jpg", 1, genre);
            await unitOfWork.AlbumRepository.AddAsync(album);

            albumAuthor = new AlbumAuthor(2, album, 2, author);
            await unitOfWork.AlbumAuthorRepository.AddAsync(albumAuthor);

            song = new Song("Слезы на ветер", "baipolar.jpg", "slezynaveter.mp3", 2, album);
            await unitOfWork.SongRepository.AddAsync(song);

            songAuthor = new SongAuthor(2, song, 2, author);
            await unitOfWork.SongAuthorRepository.AddAsync(songAuthor);

            playlistSong = new PlaylistSong(1, playlist, 2, song);
            await unitOfWork.PlaylistSongRepository.AddAsync(playlistSong);


            song = new Song("Не виноваты планеты", "baipolar.jpg", "planety.mp3", 2, album);
            await unitOfWork.SongRepository.AddAsync(song);

            songAuthor = new SongAuthor(3, song, 2, author);
            await unitOfWork.SongAuthorRepository.AddAsync(songAuthor);

            playlistSong = new PlaylistSong(1, playlist, 3, song);
            await unitOfWork.PlaylistSongRepository.AddAsync(playlistSong);

            //playlist = new Playlist("Test2", "Herman.jpg", 2, user);
            //await unitOfWork.PlaylistRepository.AddAsync(playlist);

            //playlistUser = new PlaylistUser(2, user, 2, playlist);
            //await unitOfWork.PlaylistUserRepository.AddAsync(playlistUser);

            var favouritesongs = new UserFavouriteSong(3, song, 2, user);
            await unitOfWork.UserFavouriteSongRepository.AddAsync(favouritesongs);

            ///========================================================Chopchik

            author = new Author("Дмитрий Чопиц", "Chopchik.jpg");
            await unitOfWork.AuthorRepository.AddAsync(author);

            album = new Album("Chopchik", "Chopchik.jpg", 1, genre);
            await unitOfWork.AlbumRepository.AddAsync(album);

            albumAuthor = new(3, album, 3, author);
            await unitOfWork.AlbumAuthorRepository.AddAsync(albumAuthor);

            song = new Song("Молодой Чопик", "Chopchik.jpg", "chopchik.mp3", 3, album);
            await unitOfWork.SongRepository.AddAsync(song);

            songAuthor = new SongAuthor(4, song, 3, author);
            await unitOfWork.SongAuthorRepository.AddAsync(songAuthor);

            playlistSong = new PlaylistSong(1, playlist, 4, song);
            await unitOfWork.PlaylistSongRepository.AddAsync(playlistSong);*/

            await unitOfWork.SaveAllAsync();
        }
    }
}

