from src.settings.general import GeneralSettings
from src.settings.mongo import MongoSettings


class Settings(MongoSettings, GeneralSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
