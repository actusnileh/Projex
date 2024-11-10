from settings.general import GeneralSettings
from settings.mongo import MongoSettings


class Settings(MongoSettings, GeneralSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"


settings = Settings()
