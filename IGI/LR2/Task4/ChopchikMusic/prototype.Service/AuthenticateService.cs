using System;
using System.Security.Claims;

namespace prototype.Service
{
	public class AuthenticateService
	{
		public static ClaimsIdentity Authenticate(User user)
		{
			var claims = new List<Claim>
			{
                new Claim(ClaimsIdentity.DefaultNameClaimType, user.Name),
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString())
            };
            return new(claims, "token", ClaimsIdentity.DefaultNameClaimType, ClaimTypes.NameIdentifier);
        }
    }
}

