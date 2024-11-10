from settings.general import GeneralSettings


class MongoSettings(GeneralSettings):
    MONGO_URI: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
