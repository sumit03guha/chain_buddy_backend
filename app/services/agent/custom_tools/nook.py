import requests
from pydantic import BaseModel, Field


class GetNookProfileInput(BaseModel):
    name: str = Field(..., description="Name of the Nook profile")


def get_movies_from_nook_profile(name: str) -> str:

    profile_id = get_nook_profile_id(name)

    if profile_id:
        url = f"https://nook-api.up.railway.app/entities/{profile_id}/events"

        response = requests.get(url)

        if response.status_code == 200:
            response = response.json()

            movie_reviews = {}

            for movie in response.get("results"):
                movie_reviews[movie.get("content").get("title")] = movie.get(
                    "interaction"
                ).get("review")

            return movie_reviews
        else:
            return f"Error: {response.status_code}"
    else:
        return f"Profile with name {name} not found."


def get_nook_profile_id(name: str) -> str:
    url = f"https://nook-api.up.railway.app/entities/{name}"

    response = requests.get(url)

    if response.status_code == 200:
        response = response.json()

        return response.get("id")
    else:
        return f"Error: {response.status_code}"
