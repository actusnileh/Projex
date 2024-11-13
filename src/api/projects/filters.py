from pydantic import BaseModel

from infrastructure.repositories.filters.projects import GetTasksInfraFilters


class GetTasksFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetTasksInfraFilters(
            limit=self.limit,
            offset=self.offset,
        )
