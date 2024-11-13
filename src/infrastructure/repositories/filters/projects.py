from dataclasses import dataclass


@dataclass
class GetTasksInfraFilters:
    limit: int = 10
    offset: int = 0
