from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    SERVICE_NAME: str = "Projex API"
