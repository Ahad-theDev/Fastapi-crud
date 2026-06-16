from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional
class Settings(BaseSettings):
    database_hostname: str = ""
    database_port: int = 5432
    database_password: str = ""
    database_name: str = ""
    database_username: str = ""
    database_url: Optional[str] = None  # Render provides this
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

# class Settings(BaseSettings):
#     database_url: str | None = None
#     # database_hostname:str
#     # database_port:int
#     # database_password:str
#     # database_name:str
#     # database_username:str
#     secret_key:str
#     algorithm:str
#     access_token_expire_minutes:int
    
#     # model_config = SettingsConfigDict(env_file=".env")

settings = Settings()