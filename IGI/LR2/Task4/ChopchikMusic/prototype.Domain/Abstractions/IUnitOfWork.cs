using System;
using System.Numerics;
using prototype.Domain.Entities;

namespace prototype.Domain.Abstractions
{
    public interface IUnitOfWork
    {
        IRepository<User> UserRepository { get; }
        IRepository<Album> AlbumRepository { get; }
        IRepository<AlbumAuthor> AlbumAuthorRepository { get; } 
        IRepository<Genre> GenreRepository { get; }
        IRepository<Playlist> PlaylistRepository { get; }
        IRepository<PlaylistSong> PlaylistSongRepository { get; }
        IRepository<PlaylistUser> PlaylistUserRepository { get; }
        IRepository<Song> SongRepository { get; }
        IRepository<SongAuthor> SongAuthorRepository { get; }
        IRepository<UserFavouriteAuthor> UserFavouriteAuthorRepository { get; }
        IRepository<UserFavouriteGenres> UserFavouriteGenresRepository { get; }
        IRepository<UserFavouriteSong> UserFavouriteSongRepository { get; }

        public Task SaveAllAsync();
        public Task DeleteDataBaseAsync();
        public Task CreateDataBaseAsync();

        public Task ConnectDataBaseAsync();
    }
}

