using System;
using System.Numerics;
using Microsoft.EntityFrameworkCore;
using prototype.Domain.Entities;

namespace prototype.Persistence.Data
{
	public class AppDbContext : DbContext
	{
		///Tables start
		public DbSet<User> Users { get; set; }
		public DbSet<Album> Albums { get; set; }
		public DbSet<AlbumAuthor> AlbumAuthors { get; set; }
		public DbSet<Genre> Genres { get; set; }
		public DbSet<Playlist> Playlists { get; set; }
		public DbSet<PlaylistSong> PlaylistSongs { get; set; }
		public DbSet<PlaylistUser> PlaylistUsers { get; set; }
		public DbSet<Song> Songs { get; set; }
		public DbSet<SongAuthor> SongAuthors { get; set; }
		public DbSet<UserFavouriteAuthor> UserFavouriteAuthors { get; set; }
		public DbSet<UserFavouriteGenres> UserFavouriteGenres { get; set; }
		public DbSet<UserFavouriteSong> UserFavouriteSongs { get; set; }
		///Tables end

		private readonly DbContextOptions<AppDbContext> _options;

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
            _options = options;
            Database.EnsureCreated();
        }

   //     protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
   //     {
			//optionsBuilder.UseNpgsql("Host=localhost;Port=5433;Database=musictest;Username=postgres;Password=1234");
   //     }


    }
}

