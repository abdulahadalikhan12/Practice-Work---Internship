from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Centralized app configuration.

    Pydantic's BaseSettings automatically reads matching variables from
    the .env file (or real environment variables) and validates their types.
    This means nowhere else in the app do we write open(".env") or hardcode
    "notes.txt" directly -- everyone just imports `settings` from here.
    """
    NOTES_FILE_PATH: str = "notes.txt"

    class Config:
        env_file = ".env"


# Created once, reused everywhere via FastAPI's Depends (see core/config.py usage
# in routers/notes.py). This is the "Core" piece from your diagram.
settings = Settings()
