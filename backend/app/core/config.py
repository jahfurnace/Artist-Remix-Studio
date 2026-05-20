from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vocal Remix Studio"
    API_V1_STR: str = "/api/v1"
    
    # Stripe
    STRIPE_API_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Replicate
    REPLICATE_API_TOKEN: str = ""
    
    # Database (SQLite for local dev)
    DATABASE_URL: str = "sqlite:///./vocal_remix.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
