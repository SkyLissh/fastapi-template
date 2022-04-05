from typing import Union

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    API_VERSION: str = "/api/v1"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://localhost",
    ]

    @classmethod
    @validator("BAKCEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

        raise ValueError(
            f"BACKEND_CORS_ORIGINS must be a string or list of strings, got {type(v)}"
        )

    PROJECT_NAME: str = "PROJECT_NAME"

    class Config:
        case_sensitive: bool = True


settings = Settings()
