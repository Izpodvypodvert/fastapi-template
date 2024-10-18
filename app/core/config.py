from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    host: str = ""
    secret: str = ""
    client_id: str = ""
    client_secret: str = ""
    frontend_base_url: str = ""
    frontend_login_redirect_url: str = ""
    frontend_oauth_redirect_url: str = ""
    email_address: str = ""
    email_password: str = ""
    smtp_address: str = ""
    smtp_port: str = ""
        
    class Config:
        env_file = ".env"
        
    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.host}:5432/{self.postgres_db}"

    @property
    def reset_password_url(self):
        return f"{self.frontend_base_url}/reset-password?token"
    
    @property
    def verification_url(self):
        return f"{self.frontend_base_url}/verify-email?token"
    
    
settings = Settings()
