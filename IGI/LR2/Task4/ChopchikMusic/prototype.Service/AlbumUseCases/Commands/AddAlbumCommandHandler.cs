using System;
using System.Linq.Expressions;
using prototype.Domain;

namespace prototype.Service.AlbumUseCases.Commands
{
	public class AddAlbumCommandHandler : IRequestHandler<AddAlbumCommand, BaseResponse<Album>>
	{
        private readonly IUnitOfWork _unitOfWork;
		public AddAlbumCommandHandler(IUnitOfWork unitOfWork)
		{
            _unitOfWork = unitOfWork;
		}

        public async Task<BaseResponse<Album>> Handle(AddAlbumCommand request, CancellationToken cancellationToken)
        {
            try
            {
                Expression<Func<Genre, bool>> filter = c => c.Name == request.GenreName;
                var genres = await _unitOfWork.GenreRepository.ListAsync(filter, cancellationToken);
                Genre genre = genres[0];
                Album album = new Album(request.Name, "Album.jpg", genre.Id, genre);

                await _unitOfWork.AlbumRepository.AddAsync(album, cancellationToken);

                Expression<Func<User, bool>> filter2 = c => c.Name == request.AuthorName;
                var authors = await _unitOfWork.UserRepository.ListAsync(filter2, cancellationToken);
                User author = authors[0];

                var albumAuthor = new AlbumAuthor(album.Id, album, author.Id, author);
                await _unitOfWork.AlbumAuthorRepository.AddAsync(albumAuthor, cancellationToken);
                return new BaseResponse<Album>()
                {
                    StatusCode = 200,
                    Data = album
                };
            }
            catch (Exception ex)
            {
                return new BaseResponse<Album>()
                {
                    StatusCode = 500,
                    Description = ex.Message
                };
            }
        }
    }
}

