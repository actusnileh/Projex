from settings.general import GeneralSettings


class MongoSettings(GeneralSettings):
    MONGO_DB_CONNECTION_URI: str
    MONGO_DB_ADMIN_USERNAME: str
    MONGO_DB_ADMIN_PASSWORD: str
