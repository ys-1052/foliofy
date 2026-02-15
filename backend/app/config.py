from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # AWS Cognito
    aws_region: str = "ap-northeast-1"
    cognito_user_pool_id: str
    cognito_client_id: str

    # CORS
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()  # type: ignore[call-arg]
