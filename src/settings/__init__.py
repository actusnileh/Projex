from pydantic import ConfigDict

from settings.general import GeneralSettings
from settings.mongo import MongoSettings


class Settings(MongoSettings, GeneralSettings):
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow",
    )


settings = Settings()
