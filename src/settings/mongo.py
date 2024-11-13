from pydantic import Field

from settings.general import GeneralSettings


class MongoSettings(GeneralSettings):
    MONGO_URI: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    MONGO_PROJECT_DATABASE: str = Field(default="project")
    MONGO_PROJECT_COLLECTION: str = Field(default="project")
    MONGO_TASK_COLLECTION: str = Field(default="task")
