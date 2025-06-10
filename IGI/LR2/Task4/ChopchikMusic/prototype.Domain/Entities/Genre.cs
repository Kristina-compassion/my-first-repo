using System;
namespace prototype.Domain.Entities
{
	public class Genre : Entity
	{
		public string Name { get; set; }
		public Genre()
		{
			Name = "";
		}

		public Genre(string name)
		{
			Name = name;
		}
	}
}

