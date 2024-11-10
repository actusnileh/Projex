from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    SERVICE_NAME: str = "Projex API"

    API_PORT: int
    DEBUG_PORT: int
