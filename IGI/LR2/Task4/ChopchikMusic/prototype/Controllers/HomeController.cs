using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using prototype.Domain.Jwt;
using prototype.Service.UserUseCases.Commands;
using prototype.Service.UserUseCases.Queries;

namespace prototype.Controllers;

public class HomeController : Controller
{
    private readonly IMediator _mediator;

    public HomeController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet]
    public async Task<IActionResult> Login(string login, string password)
    {    
        var result = await _mediator.Send(new GetUserByNameQuery(login, password));
        if (result.StatusCode == 200)
        {
            var now = DateTime.UtcNow;
            var jwt = new JwtSecurityToken(
                issuer: AuthOptions.ISSUER,
                audience: AuthOptions.AUDIENCE,
                notBefore: now,
                claims: result.Data.Claims,
                expires: now.Add(TimeSpan.FromMinutes(AuthOptions.LIFETIME)),
                signingCredentials: new SigningCredentials(AuthOptions.GetSymmetricSecurityKey(), SecurityAlgorithms.HmacSha256));

            var encodedJwt = new JwtSecurityTokenHandler().WriteToken(jwt);
            var userId = result.Data.FindFirst(ClaimTypes.NameIdentifier);
            var response = new
            {
                access_token = encodedJwt,
                Name = result.Data.Name,
                userId = userId.Value
            };
            return Json(response);
        }
        else return BadRequest(result.Description);
    }

    [HttpPut]
    public async Task<IActionResult> Register(string login, string email, string password)
    {
        var result = await _mediator.Send(new AddUserCommand(login, email, password, "User", "Herman.jpg"));        
        if (result.StatusCode == 200)
        {
            var now = DateTime.UtcNow;
            var jwt = new JwtSecurityToken(
                issuer: AuthOptions.ISSUER,
                audience: AuthOptions.AUDIENCE,
                notBefore: now,
                claims: result.Data.Claims,
                expires: now.Add(TimeSpan.FromMinutes(AuthOptions.LIFETIME)),
                signingCredentials: new SigningCredentials(AuthOptions.GetSymmetricSecurityKey(), SecurityAlgorithms.HmacSha256));

            var encodedJwt = new JwtSecurityTokenHandler().WriteToken(jwt);
            var userId = result.Data.FindFirst(ClaimTypes.NameIdentifier);
            var response = new
            {
                access_token = encodedJwt,
                Name = result.Data.Name,
                userId = userId.Value
            };
            return Json(response);
        }
        else return BadRequest(result.Description);        
    }  

}

