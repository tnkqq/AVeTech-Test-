from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RedisHost: str
    RedisPort: int
    
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()