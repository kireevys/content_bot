class SeriesException(BaseException):
    """Исключения Сериалов."""


class MoviesException(BaseException):
    """Исключения фильмов."""


class EpisodeAlreadyExists(SeriesException):
    """Добавляемый эпизод существует."""


class SeriesParseError(SeriesException):
    """Некорректное описание для загружаемого эпизода."""


class MovieAlreadyExists(MoviesException):
    """Добавляемый фильм существует."""


class MovieParseError(SeriesException):
    """Некорректное описание для загружаемого фильма."""
