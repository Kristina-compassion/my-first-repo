using System;
using System.Numerics;
using Microsoft.EntityFrameworkCore;
using prototype.Domain.Abstractions;
using prototype.Domain.Entities;
using prototype.Persistence.Data;

namespace prototype.Persistence.Repository
{
	public class EfUnitOfWork : IUnitOfWork
	{

        private readonly AppDbContext _context;

        private readonly Lazy<IRepository<User>> _userRepository;
        private readonly Lazy<IRepository<Album>> _albumRepository;
        private readonly Lazy<IRepository<AlbumAuthor>> _albumAuthorRepository;
        private readonly Lazy<IRepository<Genre>> _genreRepository;
        private readonly Lazy<IRepository<Playlist>> _playlistRepository;
        private readonly Lazy<IRepository<PlaylistSong>> _playlistSongRepository;
        private readonly Lazy<IRepository<PlaylistUser>> _playlistUserRepository;
        private readonly Lazy<IRepository<Song>> _songRepository;
        private readonly Lazy<IRepository<SongAuthor>> _songAuthorRepository;
        private readonly Lazy<IRepository<UserFavouriteAuthor>> _userFavouriteAuthorRepository;
        private readonly Lazy<IRepository<UserFavouriteGenres>> _userFavouriteGenresRepository;
        private readonly Lazy<IRepository<UserFavouriteSong>> _userFavouriteSongRepository;

        public EfUnitOfWork(AppDbContext context)
        {
            _context = context;
            _userRepository = new Lazy<IRepository<User>>(() => new EfRepository<User>(context));
            _albumRepository = new Lazy<IRepository<Album>>(() => new EfRepository<Album>(context));
            _albumAuthorRepository = new Lazy<IRepository<AlbumAuthor>>(() => new EfRepository<AlbumAuthor>(context)); 
            _genreRepository = new Lazy<IRepository<Genre>>(() => new EfRepository<Genre>(context));
            _playlistRepository = new Lazy<IRepository<Playlist>>(() => new EfRepository<Playlist>(context));
            _playlistSongRepository = new Lazy<IRepository<PlaylistSong>>(() => new EfRepository<PlaylistSong>(context));
            _playlistUserRepository = new Lazy<IRepository<PlaylistUser>>(() => new EfRepository<PlaylistUser>(context));
            _songRepository = new Lazy<IRepository<Song>>(() => new EfRepository<Song>(context));
            _songAuthorRepository = new Lazy<IRepository<SongAuthor>>(() => new EfRepository<SongAuthor>(context));
            _userFavouriteAuthorRepository = new Lazy<IRepository<UserFavouriteAuthor>>(() => new EfRepository<UserFavouriteAuthor>(context));
            _userFavouriteGenresRepository = new Lazy<IRepository<UserFavouriteGenres>>(() => new EfRepository<UserFavouriteGenres>(context));
            _userFavouriteSongRepository = new Lazy<IRepository<UserFavouriteSong>>(() => new EfRepository<UserFavouriteSong>(context));
            

        }

        public IRepository<User> UserRepository => _userRepository.Value;
        public IRepository<Album> AlbumRepository => _albumRepository.Value;
        public IRepository<AlbumAuthor> AlbumAuthorRepository => _albumAuthorRepository.Value;
        public IRepository<Genre> GenreRepository => _genreRepository.Value;
        public IRepository<Playlist> PlaylistRepository => _playlistRepository.Value;
        public IRepository<PlaylistSong> PlaylistSongRepository => _playlistSongRepository.Value;
        public IRepository<PlaylistUser> PlaylistUserRepository => _playlistUserRepository.Value;
        public IRepository<Song> SongRepository => _songRepository.Value;
        public IRepository<SongAuthor> SongAuthorRepository => _songAuthorRepository.Value;
        public IRepository<UserFavouriteAuthor> UserFavouriteAuthorRepository => _userFavouriteAuthorRepository.Value;
        public IRepository<UserFavouriteGenres> UserFavouriteGenresRepository => _userFavouriteGenresRepository.Value;
        public IRepository<UserFavouriteSong> UserFavouriteSongRepository => _userFavouriteSongRepository.Value;

        public async Task CreateDataBaseAsync() => await _context.Database.EnsureCreatedAsync();
        public async Task DeleteDataBaseAsync() => await _context.Database.EnsureDeletedAsync();
        public async Task SaveAllAsync() => await _context.SaveChangesAsync();

        public async Task ConnectDataBaseAsync() => await _context.Database.CanConnectAsync();
    }
}

