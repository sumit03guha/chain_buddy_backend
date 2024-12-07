from pydantic import BaseModel, Field
from tmdbv3api import Movie, TMDb

from app.config.env_vars import TMDB_API_KEY

# Initialize TMDb client
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY

# Create an instance of the Movie class
movie_instance = Movie()


class GetMovieByNameInput(BaseModel):
    name: str = Field(..., description="Name of the movie")


def get_movie_by_name(name: str) -> str:
    results = movie_instance.search(name)

    if results:
        # Get the first matching result
        movie_id = results[0].id
        details = movie_instance.details(movie_id)

        movie_info = {
            "title": details.title,
            "overview": details.overview,
            "release_date": details.release_date,
            "rating": details.vote_average,
            "genre": details.genres,
        }

        return movie_info
    else:
        return "No movie found with that title."
