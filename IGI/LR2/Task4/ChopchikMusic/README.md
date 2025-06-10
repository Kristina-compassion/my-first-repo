README.md

Сущности:
    1) User. Сущность пользователя. Имеет поля: _Id, _Name, _Email, _Password, _Role (0 - простой пользователь, 1 - автор, 2 - админ), _PathToImage (путь к аватарке), _FavouritePlaylistId - указать на айдишник плейлиста с любимыми песнями).
    2) Song. Сущность песни. Имеет поля: _Id, _Name, _GenreId, _PathToImage, _PathToSong (путь к файлу самой песни).
    3) Playlist. Сущность плейлиста. Имеет поля: _Id, _Name, _PathToImage.
    4) Genre. Сущность жанра. Имеет поля: _Id, _Name.
    5) Album. Сущность альбома. Имеет поля: _Id, _Name, _PathToImage.
    6) PlaylistSong. Сущность, которая хранит пары плейлист-песня, чтобы хранить в каких плейлистах есть какие песни.
    7) Author. Сущность автора. Хранит _Id, _Name, _PathToImage.
    8) SongAuthor. Сущность, которая хранит пары песня-автор, чтобы хранить какие песни принадлежат каким авторам.
    9) AlbumAuthor. Сущность, которая хранит пары альбом-автор, чтобы хранить какие альбомы принадлежат каким авторам.
    10) UserFavouriteSong. Сущность, которая хранит пары песня-пользовать, чтобы запоминать любимые песни пользователя.
    11) UserFavouriteAuthor. Сущность, которая хранит пары автор-пользователь, чтобы запоминать любимых автором пользователя.
    12) UserFavouriteGenres. Сущность, которая хранит пары пользователь-жанр, чтобы запоминать любимые жанры пользователя.
    13) PlaylistUser. Сущность, которая хранит пары плейлист-пользователь, чтобы запоминать плейлисты пользователя.
    14) IRepository. Обобщенный интерфейс репозитория. Определяет методы: GetByIdAsync - возвращает объект, по его id, ListAllAsync - возвращает все объекты, ListAsync - возвращает объекты по какому-то фильтру, AddAsync - добавляет объект, UpdateAsync - обновляет объект, DeleteAsync - удаляет объект, FirstOrDefaultAsync.
      15-21) Сущности репозиториев, которые реализуют интерфейс IRepository: UserRepository, LibraryRepository (для работы с любимыми плейлистами, песнями, жанрами и т.п.), SongRepository, AuthorRepository, PlaylistRepository, GenresRepository, AblumRepository).
    22) IUnitOfWork. Интерфейс класса UnitOfWork. Хранит следующие поля: _UserRepository, _SongRepository, _AuthorRepository, _PlaylistRepository, _GenresRepository, _LibraryRepository. Следующие методы для работы с бд: SaveAllAsync, DeleteDataBaseAsync, CreateDataBaseAsync.
    23) UnitOfWork. Реализация интерфейса IUnitOfWork.
    24-29) Сервисы для работы с базовыми сущностями: UserService, LibraryService, SongService, AlbumService, GenreService, PlaylistService.
    30-32) Контроллеры. UserController, LibraryController, PlaylistController.
 

