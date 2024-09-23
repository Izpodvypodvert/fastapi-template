from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    host: str = ""
    secret: str = ""
    client_id: str = ""
    client_secret: str = ""

    class Config:
        env_file = ".env"
        
    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.host}:5432/{self.postgres_db}"

settings = Settings()
