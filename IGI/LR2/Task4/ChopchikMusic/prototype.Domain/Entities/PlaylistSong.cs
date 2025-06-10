using System;
namespace prototype.Domain.Entities
{
	public class PlaylistSong : Entity
	{
		public int PlaylistId { get; set; }
		public Playlist Playlist { get; set; }

		public int SongId { get; set; }
		public Song Song { get; set; }

		public PlaylistSong()
		{
			PlaylistId = 0;
			Playlist = new Playlist();
			SongId = 0;
			Song = new Song();
		}

		public PlaylistSong(int playlistId, Playlist playlist, int songId, Song song)
		{
			PlaylistId = playlistId;
			Playlist = playlist;
			SongId = songId;
			Song = song;
		}
	}
}

