using System;
using Microsoft.IdentityModel.Tokens;
using System.Text;

namespace prototype.Domain.Jwt
{
	public class AuthOptions
	{
        public const string ISSUER = "ChopchikMusic"; // издатель токена
        public const string AUDIENCE = "MyAuthClient"; // потребитель токена
        const string KEY = "qwertyuiopasdfghjklzxcvbnm123qwertyuiopasdfghjklzxcvbnm123";   // ключ для шифрации
        public const int LIFETIME = 10; // время жизни токена - 1 минута
        public static SymmetricSecurityKey GetSymmetricSecurityKey()
        {
            return new SymmetricSecurityKey(Encoding.ASCII.GetBytes(KEY));
        }
    }
}

