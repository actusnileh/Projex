from typing import (
    Any,
    Mapping,
)

from domain.entities.projects import (
    Project,
    Task,
)
from domain.values.projects import (
    Text,
    Title,
)


def convert_task_to_document(task: Task) -> dict:
    return {
        "oid": task.oid,
        "title": task.title.as_generic_type(),
        "text": task.text.as_generic_type(),
        "created_at": task.created_at,
    }


def convert_project_to_document(project: Project) -> dict:
    return {
        "oid": project.oid,
        "title": project.title.as_generic_type(),
        "created_at": project.created_at,
    }


def convert_task_document_to_entity(task_document: Mapping[str, Any]) -> Task:
    return Task(
        oid=task_document["oid"],
        title=Title(task_document["title"]),
        text=Text(task_document["text"]),
        created_at=task_document["created_at"],
    )


def convert_project_document_to_entity(project_document: Mapping[str, Any]) -> Project:
    return Project(
        oid=project_document["oid"],
        title=Title(value=project_document["title"]),
        created_at=project_document["created_at"],
        tasks={
            convert_task_document_to_entity(task_document)
            for task_document in project_document["tasks"]
        },
    )
