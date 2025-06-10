using System;
namespace prototype.Domain.Entities
{
	public class Album : Entity
	{
        public string Name { get; set; }
        public string PathToImage { get; set; }
        public int GenreId { get; set; }
        public Genre Genre { get; set; }

        public Album()
        {

        }

        public Album(string name, string path, int genreId, Genre genre)
        {
            Name = name;
            PathToImage = path;
            GenreId = genreId;
            Genre = genre;
        }

    }
}

