using System;
namespace prototype.Domain.Entities
{
	public class User : Entity
	{
		public string? Name { get; set; }
		public string? Role { get; set; }
		public string? Password { get; set; }
		public string? Email { get; set; }
		public string? PathToImage { get; set; }

		public User(string? name, string? email, string? password, string? role, string? path)
		{
			Name = name;
			Email = email;
			Role = role;
			Password = password;
			PathToImage = path;
		}

		public User()
		{
			Name = "Андрей Черкашвский";
			Role = "Мешаю Роме спать";
			Password = "6бутылокпива";
			Email = "nagibator2012@mail.ru";
			PathToImage = "hrenovo.meni";
		}

	}
}

